#!/bin/bash

# echo "# TI-4" >> README.md
git init
git add *
git commit -m "main_src changesexcluded hte Results file for each simulations"
git branch -M main
git remote add origin https://github.com/Darz2/TI-4.git
git push -u origin main