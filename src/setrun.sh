#!/bin/bash

folder="DIR_NAME"
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
            
            if [ -d "$folder/L_${L}/block_${i}/sim_${j}" ]; then
                rm -r ${fold}
            fi

            mkdir -p ${fold}

            echo "$L"

            cp src/run                          ./
            sed -i "s/L_VAL/${L}/g"             run
            sed -i "s/Box_VAL/B_VAL/g"      run

            if (( $(echo "${L} > 0.9" | bc -l) )); then
                sed -i "s/D_VAL/0.4/g" run
            elif (( $(echo "${L} > 0.7" | bc -l) )); then
                sed -i "s/D_VAL/0.7/g" run
            else
                sed -i "s/D_VAL/1/g" run
            fi

            mv run                              ${fold}

            cp src/plot                         ./
            sed -i "s|FOLD|../../${fold}|g"     plot
            mv plot                             ${fold}

            cp src/submit_H.sh                  ./
            sed -i "2s/l/${L}/g"                 submit_H.sh
            sed -i "2s/b/${i}/2"                 submit_H.sh
            sed -i "2s/s/${j}/g"                 submit_H.sh
            mv submit_H.sh                      ${fold}

            cp src/a_1.out                        ${fold}

        done
    done
done


wait
./SUBMIT