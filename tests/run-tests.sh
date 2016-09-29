#!/bin/bash

cd $(dirname ${BASH_SOURCE[0]})

for file in [a-z]*.scm; do
  echo "=> $file"
  if [ "$1" = '-d' -o "$1" = '--debug' ]; then
    ../bin/lll $file
  else
    ../bin/lll $file | grep -v '^OK'
  fi
done
