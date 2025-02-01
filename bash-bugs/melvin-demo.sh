#!/bin/sh

echo "BASH_VERSION = $BASH_VERSION"

set -o errexit

foo() {
        set +o errexit
        if command time -f '%e' true > /dev/null;
        then
                echo 'inside'
        fi
        set -o errexit
        echo 'outside'
}

foo &

echo waiting
wait
echo done

