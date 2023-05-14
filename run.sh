#!/bin/bash

# chmod +x ./run.sh
# ./run.sh "cookie xxxxx"

if [[ "$1" != "" ]]; then
    export QPET_COOKIE="$1"
    echo "QPET_COOKIE $1"
    if command -v python3 &> /dev/null; then
        echo "python3 qpet.py"
        python3 ./src/qpet.py
    elif command -v python &> /dev/null ; then
        echo "python qpet.py"
        python ./src/qpet.py
    fi
else 
    echo "Cookie is null"
fi
