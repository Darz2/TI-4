#!/usr/bin/env python

### Importing the required libraries ###

import os
import math
import subprocess
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import trapezoid

### Defining the required functions ###

def format_value(value):
    return f"{value:.6f}"

def avg(array):
    
    sum_of_array        = sum(array)
    number_of_elements  = len(array)

    try:
        average         = sum_of_array / number_of_elements
    except ZeroDivisionError:
        average         = float('nan')

    return average

def sd(array):
    
    mean                = sum(array) / len(array)
    squared_mean        = mean ** 2
    squared_elements    = []
    
    for element in array:
        squared_element     = element ** 2
        squared_elements.append(squared_element)
    variance            = sum(squared_elements) / len(array)
    standard_deviation  = math.sqrt(variance - squared_mean)
    
    return standard_deviation

def excess_free_energy(rho, T, U, N, Q, sigma_energy, sigma_q):
    
    """
    Calculate the per-particle free energy and its uncertainty.
    
    Parameters:
    - rho : float : Density
    - T : float : Temperature
    - U : float : Internal energy
    - N : float : Number of particles
    - Q : float : The integration port in two-particles excess entropy calculations (which is a function of radial distribution function (g(r)))
    - sigma_energy : float : Uncertainty in internal energy (U)
    - sigma_q : float : Uncertainty in entropy term (Q)
    
    Returns:
    - per_particle_free_energy (fa) : float : Free energy per particle
    - sigma_per_particle (fac) : float : Uncertainty in free energy per particle
    """
    
    s_excess        = -(2 * 3.14 * rho) * Q
    sigma_s_excess  = abs(2 * 3.14 * rho) * sigma_q
    
    A               = U - T * (N * s_excess)
    sigma_A         = np.sqrt(sigma_energy**2 + (T * N * sigma_s_excess)**2)
                      
    per_particle_free_energy    = A / N
    sigma_per_particle          = sigma_A / N
    
    return s_excess, sigma_s_excess, per_particle_free_energy, sigma_per_particle

def calculate_excess_free_energy(dudl_data, T, U, N):
    
    lambda_values       = dudl_data[:, 0]
    du_dlambda_values   = dudl_data[:, 3]
    spline              = CubicSpline(lambda_values, du_dlambda_values)
    lambda_fine         = np.linspace(0, 1, 1000)
    du_dlambda_fine     = spline(lambda_fine)
    area_trapezoid      = trapezoid(du_dlambda_fine, lambda_fine)
    free_enrgy_TI       = area_trapezoid/N
    s_excess_TI         = ((U/N)-free_enrgy_TI)/T
    
    return free_enrgy_TI, s_excess_TI

def error(A_entropy, A_TI):
    
    """
    Calculate both the Absolute Percentage Error (APE) and Mean Absolute Error (MAE) for a single data point.

    Parameters:
    A_entropy (float): The excess free energy calculated from A = U -TS
    A_TI (float): The excess free energy calculated from Thermodynamic Integration

    Returns:
    tuple: The APE formatted to two decimal places and MAE formatted to four decimal places.
    """
    if A_TI == 0:
        raise ValueError("The excess free energy calculated from Thermodynamic Integration cannot be zero.")

    mae = abs(A_TI - A_entropy)
    ape = abs((A_TI - A_entropy) / A_TI) * 100
    mbe = (A_TI - A_entropy)
    
    return f"{ape:.2f}", f"{mae:.4f}", f"{mbe:.4f}"

### Output DIrecxtories ###

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
file_errors     = f"EXCESS_ENTROPY/ERROR_TP_B2.dat"

### Main Variables ###

density_1     = np.floor(np.linspace(0.01, 0.1, 10) * 100) / 100
density_2     = np.floor(np.arange(0.2, 1.0, 0.2) * 10) / 10
density       = np.concatenate((density_1, density_2))
dir_names     = [f"Rho_{i}" for i in density]
block         = 5
sim           = 2
N             = 100
T             = 4
file_paths    = [f"TP_{rho}/TP_B2.dat" for rho in density]


### Main Code ###

datasets = []
for file_path in file_paths:
    if os.path.exists(file_path):
        dudl_data = np.loadtxt(file_path, skiprows=1, usecols=(0, 1, 2, 3))
        datasets.append(dudl_data)
    else:
        print(f"File {file_path} not found.")


for i, dudl_data in enumerate(datasets):
    
    D = dir_names[i]
    r = density[i]
    
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
    avgb_rho    = round(avg(rho_b),2)
    avgb_box    = round(avg(box_b),2)
    avgb_energy = round(avg(energy_b),6)
    avgb_qgr    = round(avg(qgr_b),6)
    avgb_qgrc   = round(avg(qgrc_b),6)
    
    # sd_rho    = round(sd(rho_b),6)
    sd_energy   = round(sd(energy_b),6)
    sd_qgr      = round(sd(qgr_b),6)
    sd_qgrc     = round(sd(qgrc_b),6)
    
    s_excess, sd_s_excess, fa, sd_fa       = excess_free_energy(avgb_rho, T, avgb_energy, N, avgb_qgr, sd_energy, sd_qgr)
    s_excess_c, sd_s_excess_c, fac, sd_fac = excess_free_energy(avgb_rho, T, avgb_energy, N, avgb_qgrc, sd_energy, sd_qgrc)
    
    excess_free_energy_TI, s_excess_TI     = calculate_excess_free_energy(dudl_data, T, avgb_energy, N)
    
    FE_ape, FE_mae, FE_mbe                  = error(fa, excess_free_energy_TI)
    FE_ape_c, FE_mae_c, FE_mbe_c            = error(fac, excess_free_energy_TI)
    
    SEX_ape, SEX_mae, SEX_mbe               = error(s_excess, s_excess_TI)
    SEX_ape_c, SEX_mae_c, SEX_mbe_c         = error(s_excess_c, s_excess_TI)
    
    print(f"Excess Free Energy with TI      for {avgb_rho:.2f}: {excess_free_energy_TI:.6f}")
    print(f"Excess Free energy with g       for {avgb_rho:.2f}: {fa:.6f}")
    print(f"Error without correction        for {avgb_rho:.2f}: {FE_mae}")
    print(f"Excess Free enregy with g_infty for {avgb_rho:.2f}: {fac:.6f}")
    print(f"Error with correction           for {avgb_rho:.2f}: {FE_mae_c}")
    
    if not os.path.isfile(file_properties):  
        with open(file_properties, "w") as file:  
            file.write("Rho   Box   Energy/N      qs     qs_c    S_ex      S_ex_c    S_ex_TI   FE/N    FE_c/N  FE_TI/N\n")
            file.write(f"{avgb_rho} {avgb_box} {format_value(avgb_energy/N)} {format_value(avgb_qgr)} {format_value(avgb_qgrc)} {format_value(s_excess)} {format_value(s_excess_c)} {format_value(s_excess_TI)} {format_value(fa)} {format_value(fac)} {format_value(excess_free_energy_TI)}\n") 
    else:
        with open(file_properties, "a") as file:  
            file.write(f"{avgb_rho} {avgb_box} {format_value(avgb_energy/N)} {format_value(avgb_qgr)} {format_value(avgb_qgrc)} {format_value(s_excess)} {format_value(s_excess_c)} {format_value(s_excess_TI)} {format_value(fa)} {format_value(fac)} {format_value(excess_free_energy_TI)}\n")  


    if not os.path.isfile(file_errors):  
        with open(file_errors, "w") as file:  
            file.write("Rho  FE_APE  FE_APE_c  FE_MAE   FE_MAE_c   FE_MBE   FE_MBE_c SEX_APE SEX_APE_c  SEX_MAE  SEX_MAE_c  SEX_MBE  SEX_MBE_c\n")
            file.write(f"{avgb_rho} {FE_ape} {FE_ape_c} {FE_mae} {FE_mae_c} {FE_mbe} {FE_mbe_c} {SEX_ape} {SEX_ape_c} {SEX_mae} {SEX_mae_c} {SEX_mbe} {SEX_mbe_c}\n") 
    else:
        with open(file_errors, "a") as file:  
            file.write(f"{avgb_rho} {FE_ape} {FE_ape_c} {FE_mae} {FE_mae_c} {FE_mbe} {FE_mbe_c} {SEX_ape} {SEX_ape_c} {SEX_mae} {SEX_mae_c} {SEX_mbe} {SEX_mbe_c}\n")  

            
    if not os.path.isfile(file_sd):  
        with open(file_sd, "w") as file:  
            file.write("Rho  Energy/N   qs      qs_c       S_ex     S_ex_c    FE    FE_c\n")
            file.write(f"{avgb_rho} {format_value(sd_energy/N)} {format_value(sd_qgr)} {format_value(sd_qgrc)} {format_value(sd_s_excess)} {format_value(sd_s_excess_c)} {format_value(sd_fa)} {format_value(sd_fac)}\n")
    else:
        with open(file_sd, "a") as file:  
            file.write(f"{avgb_rho} {format_value(sd_energy/N)} {format_value(sd_qgr)} {format_value(sd_qgrc)} {format_value(sd_s_excess)} {format_value(sd_s_excess_c)} {format_value(sd_fa)} {format_value(sd_fac)}\n")