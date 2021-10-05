#
# Portable Library
#

readonly GLOB_TMP=_tmp/glob-backtrack

repeat() {
  local s=$1
  local n=$2

  for i in $(seq $n); do
    echo -n "$s"
  done
}

glob_bench() {
  local max=${1:-5}
  cd $GLOB_TMP

  for i in $(seq $max); do
    local pat="$(repeat 'a*' $i)b"
    time echo $pat
    echo
  done
}

fnmatch_task() {
  local text=$1
  local pat=$2

  case $text in
    ($pat)
      echo yes
      ;;
    (*)
      echo no
      ;;
  esac
}

fnmatch_bench() {
  local max=${1:-5}
  cd $GLOB_TMP

  # hm this never matches?
  local text=$(repeat a 100)
  for i in $(seq $max); do
    local pat="$(repeat 'a*' $i)b"
    time fnmatch_task "$text" "$pat"
    echo
  done
}

ext_fnmatch_bench() {
  local max=${1:-20}
  local workload=${2:-glob}
  cd $GLOB_TMP

  shopt -s extglob

  for i in $(seq $max); do
    case $workload in
      # backtracks in both bash and OSH
      # I think mksh doesn't do this dynamic globbing
      glob)
        # matching a^N b against a^100
        # like fnmatch workload above

        local text=$(repeat a 100)
        local pat=$(repeat 'a?(a)' $i)b
        ;;

      # backtracks when it does NOT Match, i.e. when the text is a^N b, not
      # just a^N
      regex)
        # Using the regex workload rather than the glob workload
        # https://swtch.com/~rsc/regexp/regexp1.html

        # matching a?^N a^N again a^N
        local text=$(repeat a $i)b
        local pat="$(repeat '?(a)' $i)$(repeat 'a' $i)"
        ;;
    esac

    echo $i "$text" "$pat"
    time fnmatch_task "$text" "$pat"
    echo
  done
}



