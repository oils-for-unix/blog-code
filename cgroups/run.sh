#!/usr/bin/env bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

work() {
  trap 'echo "(b) $BASHPID got SIGTERM"' TERM
  echo "> PID $BASHPID sleep $1"
  sleep $1 
  echo "< sleep $1"
}

fork-recklessly() {
  for t in 0.{1..9}; do
    work $t &
  done
  wait
  echo '<<< fork'
}

shell-term-kill() {
  # create a new control group

  local group=/sys/fs/cgroup/cgroup-demo

  sudo mkdir -p $group

  # put this shell process in the group
  echo $$ | sudo tee $group/cgroup.procs

  #trap 'echo "(a) $BASHPID got SIGTERM"; exit' TERM

  # all children are in the group
  fork-recklessly &

  sleep 0.5

  sudo cat $group/cgroup.procs | xargs --verbose -- kill -TERM || true

  sleep 0.5

  # kill it atomically; SIGKILL can't be handled
  echo 1 | sudo tee $group/cgroup.kill

  echo '<<< demo'
}

rootless-with-systemd() {
  systemd-run --user --scope --unit my-demo -- $0 fork-recklessly &
  sleep 0.2

  systemctl --user list-units --type=scope
  sleep 0.2

  # Kill as user
  systemctl --user kill --signal=TERM my-demo.scope
  sleep 0.2

  #systemctl --user kill --signal=KILL my-demo.scope
}

# Why does this work without root?  Claude says it uses DBus to the systemd daemon:

# # systemd-run sends a message like this over D-Bus:
# busctl --user call \
#   org.freedesktop.systemd1 \
#   /org/freedesktop/systemd1 \
#   org.freedesktop.systemd1.Manager \
#   StartTransientUnit \
#   "ssa(sv)a(sa(sv))" \
#   "my-scope.scope" "replace" 2 \
#   "PIDs" "au" 1 $$ \
#   "Slice" "s" "user.slice"

"$@"
