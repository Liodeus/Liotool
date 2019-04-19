#!/bin/bash

while read payload; do
    if curl -vs "$1/$payload" 2>&1 | grep -i '^< Set-Cookie: crlf' &> /dev/null; then 
        echo "[+]$1/$payload"
    else
        echo "[-]$1/$payload"
    fi
done < $2

printf "\n-- Done --"
