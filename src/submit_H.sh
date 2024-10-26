#!/bin/bash
#SBATCH --job-name=LAMBDA_l_BLOCK_b_SIM_s
#SBATCH -p serial
#SBATCH -n 1
#SBATCH --mem-per-cpu=2G
#SBATCH -t 6-00:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=d.raju.tudelft.nl

./run > sim.log 

wait