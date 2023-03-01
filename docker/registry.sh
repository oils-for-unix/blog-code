#!/bin/bash 

registry_url='https://registry-1.docker.io'
auth_url='https://auth.docker.io'
svc_url='registry.docker.io'

log() {
  echo "$@" >&2
}

my-curl() {
  # -f fail silently
  # -s silent
  # -S show error
  # -L follow redirects

  #curl -f -s -S -L "$@"

  curl -L "$@"
}

# Hm this appears to do no validation at all, the scope can be anything
auth_token2() { 
  local image=$1
  my-curl "${auth_url}/token?service=${svc_url}&scope=repository:${image}:pull" \
    | jq --raw-output .token
}

manifest2() { 
  local token=$1
  local image=$2
  local digest=${3:-latest}

  my-curl \
    -H "Authorization: Bearer $token" \
    -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
    -H 'Accept: application/vnd.docker.distribution.manifest.v1+json' \
    -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
      "${registry_url}/v2/${image}/manifests/${digest}"
}

blob() {
  local token=$1
  local image=$2
  local digest=$3
  local file=$4

  log "$image $token -> $file"

  my-curl \
      -o "$file" \
      -H "Authorization: Bearer $token" \
      "${registry_url}/v2/${image}/blobs/${digest}"
}

linux_version() { 
  echo "$1" | jq --raw-output '.manifests[] | select(.platform.architecture=="amd64") | select(.platform.os=="linux") | .digest'
}

layers() { 
  echo "$1" | jq --raw-output '.layers[].digest'
}

config() {
  echo "$1" | jq --raw-output '.config.digest' 
}

pull() {
  local image="${1:-library/golang}"

  local token=$(auth_token2 "$image")
  local amd64=$(linux_version $(manifest2 "$token" "$image"))
  local mf=$(manifest2 "$token" "$image" "$amd64")

  local dir=_tmp/$image
  mkdir -p $dir

  # Retrieve the config blob
  local out=$dir/config.json
  blob "$token" "$image" $(config "$mf") $out

  # Retrieve each layer

  local i=0
  for L in $(layers "$mf"); do
    local out="$dir/layer_${i}.tar.gz"
    blob "$token" "$image" "$L" $out
    i=$((i + 1))
  done
}

# TODO:
# - Get debian:buster-slim ?  That's a different label?
# - Get history of uploads, not just the latest ones?

fetch-manifest() {
  local image="${1:-library/golang}"

  # TODO: can we cache these?

  local token
  token=$(auth_token2 "$image")
  #token=$(auth_token oilshell)
  log "token $token"

  local latest
  latest=$(manifest2 "$token" "$image")

  local amd64
  amd64=$(linux_version $latest)

  local mf

  local dir=_tmp/$image
  mkdir -p $dir
  manifest2 "$token" "$image" "$amd64" | tee $dir/manifest.json
}

sizes() {
  local manifest=$1

  echo $'SIZE\tDIGEST'

  cat $manifest | jq --raw-output '.layers[] | [.size, .digest] | @tsv '
}

"$@"

