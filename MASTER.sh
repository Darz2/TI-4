#!/bin/bash


#SBATCH --job-name=MASTER
#SBATCH -p serial
#SBATCH -n 1
#SBATCH --mem-per-cpu=2G
#SBATCH -t 6-00:00:00

# Rho=(0.01 0.02 0.03 0.04 0.05)
# Rho=(0.03 0.04 0.05)
# Rho=(0.06 0.07 0.08 0.09 0.1)
# Rho=(0.8 1.0)
Rho=(1.5 2.0 2.5 3.0)

# for R in ${Rho[@]}
# do  

#     ./setrun_rho_${R}.sh 
#     wait

# done 

# wait 

for R in ${Rho[@]}
do  

    sbatch setsubmit_rho_${R}.sh 
    wait

done 