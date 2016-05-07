#!/bin/bash

for f in [^_]*.py
do
    echo
    echo
    echo
    echo "Testing $f..."
    echo
    python $f
done
