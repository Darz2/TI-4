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

def excess_free_energy(rho, T, U, N, Q):
    s_excess = -(2 * 3.14 * rho) * Q
    A = U - T * (N * s_excess)
    per_particle_free_energy = A / N
    return per_particle_free_energy

bash_code = f'''
DIR_NAME="EXCESS_ENTROPY"

if [ -d "$DIR_NAME" ]; then
    rm -r "$DIR_NAME"
fi

mkdir "$DIR_NAME"
'''
subprocess.call(bash_code, shell=True)

file_properties = f"EXCESS_ENTROPY/TP_B2.dat"
file_sd         = f"EXCESS_ENTROPY/SD_TP_B2.dat"

density     = [0.01, 0.02, 0.05]
dir_names   = [f"Rho_{i}" for i in density]
block           = 5
sim             = 2
N               = 100
T               = 4

for D, r in zip(dir_names,density):
    
    rho_b    = []
    energy_b = []
    box_b    = []
    qgr_b    = []
    qgrc_b   = []
    prob_b   = []
    
    for i in range(1, block + 1):
        
        rho_s    = []
        energy_s = []
        box_s    = []
        qgr_s    = []
        qgrc_s   = []
        prob_s   = []
        
        for j in range(1, sim + 1):
            
            fold = f"{D}/L_1.00/block_{i}/sim_{j}"
            os.chdir(fold)
            
            tp_box      = subprocess.check_output(["grep", "Box", "sim.log"]).decode()
            tp_rho      = subprocess.check_output(["grep", "Rho", "sim.log"]).decode()
            tp_energy   = subprocess.check_output(["grep", "Average Energy", "sim.log"]).decode()
            tp_qr       = subprocess.check_output(["tail", "-n", "1", "Integral"]).decode()
            tp_prob     = subprocess.check_output(["grep", "Frac. Acc. Displ.", "sim.log"]).decode()
            
            # print(tp_prob)
            rho         = float(tp_rho.split()[2])
            box         = float(tp_box.split()[2])
            energy      = float(tp_energy.split()[3])
            qgr         = float(tp_qr.split()[1])
            qgrc        = float(tp_qr.split()[2])
            prob        = float(tp_prob.split()[4])
            # print(qgrc)
            
            rho_s.append(rho)
            box_s.append(box)
            energy_s.append(energy)
            qgr_s.append(qgr)
            qgrc_s.append(qgrc)
            prob_s.append(prob)
            
            # print(virial)
            os.chdir("../../../..")
        
        avgs_rho    = avg(rho_s)
        avgs_box    = avg(box_s)
        avgs_energy = avg(energy_s)
        avgs_qgr    = avg(qgr_s)
        avgs_qgrc   = avg(qgrc_s)
        avgs_prob = avg(prob_s)
        
        rho_b.append(avgs_rho)
        box_b.append(avgs_box)
        energy_b.append(avgs_energy)
        qgr_b.append(avgs_qgr)
        qgrc_b.append(avgs_qgrc)
        prob_b.append(avgs_prob)
    
    # print(prob_b)
    avgb_rho    = round(avg(rho_b),6)
    avgb_box    = round(avg(box_b),6)
    avgb_energy = round(avg(energy_b),6)
    avgb_qgr    = round(avg(qgr_b),6)
    avgb_qgrc   = round(avg(qgrc_b),6)
    
    # sd_rho    = round(sd(rho_b),6)
    sd_energy = round(sd(energy_b),6)
    sd_qgr    = round(sd(qgr_b),6)
    sd_qgrc   = round(sd(qgrc_b),6)
    
    fa        = excess_free_energy(avgb_rho, T, avgb_energy, N, avgb_qgr)
    fac       = excess_free_energy(avgb_rho, T, avgb_energy, N, avgb_qgrc)
    
    print(f"Excess free enrgy without correction {avgb_rho} is the {fa}")
    print(f"Excess free enrgy with correction {avgb_rho} is the {fac}")
    
    if not os.path.isfile(file_properties):  
        with open(file_properties, "w") as file:  
            file.write("Box rho energy qs qs_van_der_vegt Free_energy Free_energy_corrected Acc.prob\n")
            file.write(f"{avgb_box} {avgb_rho} {avgb_energy} {avgb_qgr} {avgb_qgrc} {fa} {fac} {prob_b}\n") 
    else:
        with open(file_properties, "a") as file:  
            file.write(f"{avgb_box} {avgb_rho} {avgb_energy} {avgb_qgr} {avgb_qgrc} {fa} {fac} {prob_b}\n")  
            
    if not os.path.isfile(file_sd):  
        with open(file_sd, "w") as file:  
            file.write("rho energy qs qs_van_der_vegt\n")
            file.write(f"{avgb_rho} {sd_energy} {sd_qgr} {sd_qgrc}\n") 
    else:
        with open(file_sd, "a") as file:  
            file.write(f"{avgb_rho} {sd_energy} {sd_qgr} {sd_qgrc}\n")