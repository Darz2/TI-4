#!/bin/bash

folder="Rho_0.1"
src="src"
block=5
sim=2
lambda=($(seq 0.01 0.01 1.00))

for L in ${lambda[@]}
do
    for ((i=1; i<=block; i++))
    do
        for ((j=1; j<=sim; j++))
        do

            fold="$folder/L_${L}/block_${i}/sim_${j}"
            cd ${fold}

            sbatch submit_H.sh

            cd -
        done
    done
done


