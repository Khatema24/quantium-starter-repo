#!/bin/bash

# 1. Activate the project virtual environment
# Since you are on Windows using Git Bash/PowerShell, we target the Scripts folder
source venv/Scripts/activate

# 2. Execute the test suite
pytest -v -s

# 3. Capture the exit status of pytest
# $? is a special variable in bash that holds the exit code of the last command
TEST_RESULT=$?

# Check if tests passed or failed and return the correct exit code
if [ $TEST_RESULT -eq 0 ]; then
    echo "CI Status: All tests passed successfully! Exiting with code 0."
    exit 0
else
    echo "CI Status: Tests failed! Exiting with code 1."
    exit 1
fi