#!/bin/bash

# This script is used to generate the plots for all the python3 file sin the directory

for file in *.py
do
    # echo "Processing $file"
    python3 $file
    code *.jpg
done