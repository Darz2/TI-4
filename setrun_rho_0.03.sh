#!/bin/bash

#SBATCH --job-name=setrun_rho_0.01
#SBATCH -p serial
#SBATCH -n 1
#SBATCH --mem-per-cpu=2G
#SBATCH -t 6-00:00:00

folder="Rho_0.03"
src="src"
block=5
sim=2
lambda=($(seq 0.01 0.01 1.00))
Alpha=1.0d0
Rcut=2.0d0


for L in ${lambda[@]}
do
    for ((i=1; i<=block; i++))
    do
        for ((j=1; j<=sim; j++))
        do

            fold="$folder/L_${L}/block_${i}/sim_${j}"
            
            if [ -d "$folder/L_${L}/block_${i}/sim_${j}" ]; then
                rm -r ${fold}
            fi

            mkdir -p ${fold}

            echo "$L"

            cp src/run                          ./
            sed -i "s/L_VAL/${L}/g"             run
            sed -i "s/Box_VAL/14.938016/g"          run
            sed -i "s/A_VAL/$Alpha/g"           run
            sed -i "s/R_VAL/$Rcut/g"            run

            if (( $(awk 'BEGIN {print ('"$L"' > 0.9)}') )); then
                sed -i "s/D_VAL/7/g" run
            elif (( $(awk 'BEGIN {print ('"$L"' > 0.7)}') )); then
                sed -i "s/D_VAL/7/g" run
            else
                sed -i "s/D_VAL/7/g" run
            fi

            mv run                              ${fold}

            cp src/plot                         ./
            sed -i "s|FOLD|../../${fold}|g"     plot
            mv plot                             ${fold}

            cp src/submit_H.sh                  ./
            sed -i "2s/r/${folder}/g"           submit_H.sh
            sed -i "2s/l/${L}/g"                submit_H.sh
            sed -i "2s/b/${i}/2"                submit_H.sh
            sed -i "2s/s/${j}/g"                submit_H.sh
            mv submit_H.sh                      ${fold}

            cp src/a.out                        ${fold}

        done
    done
done


wait
# ./setsubmit_rho_0.03.sh