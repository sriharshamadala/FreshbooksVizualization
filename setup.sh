#!/bin/bash

# Initialize the submodules.
git submodule update --init --recursive

# Create empty __init.py file in freshbooks api for importing it as a module.
touch "./FreshbooksPython/__init__.py"

# Execute the script
python MyFreshbooks.py $1 $2 > $3

# Open the output file using default application.
if [ "$(uname)" == "Darwin" ]; then
    # OSx:
    open $3
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux:
    xdg-open $3
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # If windows:
    start $3
elif [[ $(uname -s) == CYGWIN* ]]; then
    # cygwin:
    cygstart $3
fi



