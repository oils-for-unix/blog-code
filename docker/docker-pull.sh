#!/bin/bash 

image="${1:-golang}"
registry_url='https://registry-1.docker.io'
auth_url='https://auth.docker.io'
svc_url='registry.docker.io'

function auth_token { 
  curl -fsSL "${auth_url}/token?service=${svc_url}&scope=repository:library/${image}:pull" | jq --raw-output .token
}

function manifest { 
  token="$1"
  image="$2"
  digest="${3:-latest}"

  curl -fsSL \
    -H "Authorization: Bearer $token" \
    -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
    -H 'Accept: application/vnd.docker.distribution.manifest.v1+json' \
    -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
      "${registry_url}/v2/library/${image}/manifests/${digest}"
}

function blob {
  token="$1"
  image="$2"
  digest="$3"
  file="$4"

  curl -fsSL -o "$file" \
      -H "Authorization: Bearer $token" \
        "${registry_url}/v2/library/${image}/blobs/${digest}"
}

function linux_version { 
  echo "$1" | jq --raw-output '.manifests[] | select(.platform.architecture=="amd64") | select(.platform.os=="linux") | .digest'
}

function layers { 
  echo "$1" | jq --raw-output '.layers[].digest'
}

function config {
  echo "$1" | jq --raw-output '.config.digest' 
}

token=$(auth_token "$image")
amd64=$(linux_version $(manifest "$token" "$image"))
mf=$(manifest "$token" "$image" "$amd64")
blob "$token" "$image" $(config "$mf") config.json

i=0
for L in $(layers "$mf"); do
  blob "$token" "$image" "$L" "layer_${i}.tgz"
  i=$((i + 1 ))
done
