#!/bin/bash

N=100
# Rho=($(seq 0.01 0.01 0.02))
# Rho=(0.01 0.02 0.03 0.04 0.05 0.1 0.15 0.2 0.4 0.6)
Rho=(0.01 0.02 0.03 0.04 0.05)


for R in ${Rho[@]}
do  
    echo "Rho = $R"
    cp src/setrun.sh                            ./
    cp src/setsubmit.sh                         ./

    mv setrun.sh                                setrun_rho_${R}.sh
    mv setsubmit.sh                             setsubmit_rho_${R}.sh

    tmp=$(echo "$N / $R" | bc -l)
    L=$(echo "e(l($tmp)/3)" | bc -l | awk '{printf "%.6f", $0}')

    sed -i "s/DIR_NAME/Rho_${R}/g"              setrun_rho_${R}.sh
    sed -i "s/B_VAL/${L}/g"                     setrun_rho_${R}.sh
    sed -i "s/SUBMIT/setsubmit_rho_${R}.sh/g"   setrun_rho_${R}.sh

    sed -i "s/DIR_NAME/Rho_${R}/g"              setsubmit_rho_${R}.sh
    
done 