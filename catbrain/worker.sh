#!/bin/sh
# worker.sh - Prints each argument as a netstring with sleep interval between them

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <sleep_interval> [arg1] [arg2] ..." >&2
    exit 1
fi

# Store the sleep interval and shift it out from the argument list
sleep_interval="$1"
shift

echo "WORKER $$ sleeping $sleep_interval with $# args" >&2

# Process each argument
for arg in "$@"; do
    # Calculate the length of the argument
    arg_length=${#arg}
    
    # Print the netstring format: <length>:<contents>,
    printf "%d:%s," "$arg_length" "$arg"
    
    # Sleep for the specified interval
    sleep "$sleep_interval"
done
