#!/usr/bin/env python

import os
import math
import subprocess
import numpy as np

def avg(array):
    sum_of_array = sum(array)
    number_of_elements = len(array)

    try:
        average = sum_of_array / number_of_elements
    except ZeroDivisionError:
        average = float('nan')

    return average

def sd(array):
    mean = sum(array) / len(array)
    squared_mean = mean ** 2
    squared_elements = []
    for element in array:
        squared_element = element ** 2
        squared_elements.append(squared_element)
    variance = sum(squared_elements) / len(array)
    standard_deviation = math.sqrt(variance - squared_mean)
    return standard_deviation

bash_code = '''
DIR_NAME="TP_0.02"

if [ -d "$DIR_NAME" ]; then
    rm -r "$DIR_NAME"
fi

mkdir "$DIR_NAME"
'''
subprocess.call(bash_code, shell=True)

dir_name        = ["Rho_0.02"]
lambda_values   = np.round(np.arange(0.01, 1.01, 0.01), 2)
lambda_values   = [f"{value:.2f}" for value in lambda_values]
block           = 5
sim             = 2

file_properties = f"TP_0.02/TP_B2.dat"
file_sd         = f"TP_0.02/SD_TP_B2.dat"

for L in lambda_values:
    
    print(L)
    rho_b    = []
    energy_b = []
    dudl_b   = []
    virial_b = []
    prob_b   = []
        
    for i in range(1, block + 1):
            
        rho_s    = []
        energy_s = []
        dudl_s   = []
        virial_s = []
        prob_s   = []
                
        for j in range(1, sim + 1):
            
            fold = f"{dir_name[0]}/L_{L}/block_{i}/sim_{j}"
            os.chdir(fold)
            tp_rho      = subprocess.check_output(["grep", "Rho", "sim.log"]).decode()
            tp_energy   = subprocess.check_output(["grep", "Average Energy", "sim.log"]).decode()
            tp_dudl     = subprocess.check_output(["grep", "Average dUdL", "sim.log"]).decode()
            tp_virial   = subprocess.check_output(["grep", "Average Virial", "sim.log"]).decode()
            tp_prob     = subprocess.check_output(["grep", "Frac. Acc. Displ.", "sim.log"]).decode()
            
            # print(tp_prob)
            rho         = float(tp_rho.split()[2])
            energy      = float(tp_energy.split()[3])
            dudl        = float(tp_dudl.split()[3])
            virial      = float(tp_virial.split()[3])
            prob        = float(tp_prob.split()[4])
            # print(prob)
            
            rho_s.append(rho)
            energy_s.append(energy)
            dudl_s.append(dudl)
            virial_s.append(virial)
            prob_s.append(prob)
            
            # print(virial)
            os.chdir("../../../..")
        
        avgs_rho    = avg(rho_s)
        avgs_energy = avg(energy_s)
        avgs_dudl   = avg(dudl_s)
        avgs_virial = avg(virial_s)
        avgs_prob = avg(prob_s)
        
        rho_b.append(avgs_rho)
        energy_b.append(avgs_energy)
        dudl_b.append(avgs_dudl)
        virial_b.append(avgs_virial)
        prob_b.append(avgs_prob)
    
    print(prob_b)
    avgb_rho    = round(avg(rho_b),6)
    avgb_energy = round(avg(energy_b),6)
    avgb_dudl   = round(avg(dudl_b),6)
    avgb_virial = round(avg(virial_b),6)
    
    # sd_rho    = round(sd(rho_b),6)
    sd_energy = round(sd(energy_b),6)
    sd_dudl   = round(sd(dudl_b),6)
    sd_virial = round(sd(virial_b),6)
    
    if not os.path.isfile(file_properties):  
        with open(file_properties, "w") as file:  
            file.write("L rho energy dudl virial\n")
            file.write(f"{L} {avgb_rho} {avgb_energy} {avgb_dudl} {avgb_virial} {prob_b}\n") 
    else:
        with open(file_properties, "a") as file:  
            file.write(f"{L} {avgb_rho} {avgb_energy} {avgb_dudl} {avgb_virial} {prob_b}\n")  
            
    if not os.path.isfile(file_sd):  
        with open(file_sd, "w") as file:  
            file.write("L rho energy dudl virial\n")
            file.write(f"{L} {sd_energy} {sd_dudl} {sd_virial}\n") 
    else:
        with open(file_sd, "a") as file:  
            file.write(f"{L} {sd_energy} {sd_dudl} {sd_virial}\n")