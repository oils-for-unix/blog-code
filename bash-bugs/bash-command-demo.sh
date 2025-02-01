#!/bin/bash
# From Claude AI

set -e

# Test script to demonstrate command builtin behavior in Bash 3.2
# This shows how 'command' can exit prematurely in certain conditions

# Function to test command behavior
test_command() {
    # This will work as expected
    echo "Testing normal command usage:"
    command ls /etc/passwd
    echo "Command completed"

    # This might exit early in Bash 3.2
    echo -e "\nTesting problematic case:"
    command ls /nonexistent 2>/dev/null
    echo "This line might not be reached in Bash 3.2"
}

# Execute the test
echo "Bash version: $BASH_VERSION"
test_command
