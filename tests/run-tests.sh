#!/bin/bash

cd $(dirname ${BASH_SOURCE[0]})

for file in [a-z]*.scm; do
  echo "=> $file"
  ../bin/lll $file
done
