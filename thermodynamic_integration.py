#!/usr/bin/env python

########################### import the packages ############################
import sys
import os
import math
import numpy as np
import scienceplots
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import ScalarFormatter, MultipleLocator
from scipy.interpolate import CubicSpline
from scipy.integrate import trapezoid
import matplotlib.cm as cm

markers = ['o', 's', '^', 'D', 'h', '*', 'X' , "8"]
plot_size = (4, 3)
graphic_font = 'Arial'
math_font = 'dejavuserif'  #['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']
spine_width = 1
markersize=2
capsize=3
markeredgewidth=0.75
legend_linewidth = 1
linewidth =1                
tick_width=0.75
tick_length=4
minor_tick_width= 0.5
minor_tick_length=2
tick_labelsize=10
legend_fontsize=8
legend_boxwidth=0.75
label_fontsize=14
borderaxespad=0.6
alpha = 1
CO2_color = '#e41a1c'
MIX_color = '#008000'
rgba_CO2_color = mcolors.to_rgba(CO2_color)
rgba_MIX_color = mcolors.to_rgba(MIX_color)
CO2_face_color = (rgba_CO2_color[0], rgba_CO2_color[1], rgba_CO2_color[2], 0.6)
MIX_face_color = (rgba_MIX_color[0], rgba_MIX_color[1], rgba_MIX_color[2], 0.6)
resolution_value = 1200
break_threshold = 10 # for NIST data
plt.rcParams['font.serif'] = graphic_font
plt.rcParams['mathtext.fontset'] = math_font

N = 100
T = 4

def calculate_excess_free_energy(dudl_data):
    lambda_values = dudl_data[:, 0]
    du_dlambda_values = dudl_data[:, 3]
    spline = CubicSpline(lambda_values, du_dlambda_values)
    lambda_fine = np.linspace(0, 1, 1000)
    du_dlambda_fine = spline(lambda_fine)
    area_trapezoid = trapezoid(du_dlambda_fine, lambda_fine)
    return area_trapezoid/N

base_path = "./"
# rho_values = [0.06, 0.07, 0.08, 0.09, 0.1]
rho_values_1 = np.floor(np.arange(0.01, 0.11, 0.01) * 100) / 100
rho_values_2 = np.floor(np.arange(0.2, 1.1, 0.2) * 10) / 10
rho_values_3 = [1.5]
rho_values   = np.concatenate((rho_values_1, rho_values_2, rho_values_3))
file_paths   = [f"TP_{rho}/TP_B2.dat" for rho in rho_values]

datasets = []
for file_path in file_paths:
    if os.path.exists(file_path):
        dudl_data = np.loadtxt(file_path, skiprows=1, usecols=(0, 1, 2, 3))
        datasets.append(dudl_data)
    else:
        print(f"File {file_path} not found.")

output_file_path = os.path.join(os.getcwd(), "thermodynamic_integration.dat")
with open(output_file_path, "w") as file:
    for i, dudl_data in enumerate(datasets):
        excess_energy = calculate_excess_free_energy(dudl_data)
        result_line = f"Excess Free Energy for Rho = {rho_values[i]:.2f}: {excess_energy:.6f}"
        print(result_line)
        file.write(f"{rho_values[i]:.2f} {excess_energy:.6f}\n")

with plt.style.context([ 'ieee']):
    plt.rcParams['font.family'] = graphic_font
    plt.rcParams['mathtext.fontset'] = math_font
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize=plot_size)
    ax.spines['top'].set_linewidth(spine_width)    
    ax.spines['bottom'].set_linewidth(spine_width) 
    ax.spines['left'].set_linewidth(spine_width)   
    ax.spines['right'].set_linewidth(spine_width)  
    
    colormap = cm.get_cmap('tab10', len(datasets))  # Use a color map for more colors
    labels = [f'$\\rho$ = {rho:.2f}' for rho in rho_values]
    
    for i, dudl_data in enumerate(datasets):
        ax.plot(dudl_data[:, 0], dudl_data[:, 3],
                linestyle='solid',
                marker='s',
                markersize=6,  # Replace with markersize if defined
                color=colormap(i),
                label=labels[i])
    
    plt.xlabel(r'$\lambda$', fontsize=label_fontsize)
    plt.ylabel(r'$\langle\frac{du}{d\lambda}\rangle$',fontsize=label_fontsize)
    
    # plt.xlim(0, 0.5)
    # plt.ylim(-3, -2.5)
    # ax.xaxis.set_major_locator(MultipleLocator(0.2))
    # ax.xaxis.set_minor_locator(MultipleLocator(10))
    
    ax.tick_params(axis='both', which='major', direction='in', width=tick_width, length=tick_length, labelsize=tick_labelsize,
                bottom=True, top=True, left=True, right=True)
    ax.tick_params(axis='both', which='minor', direction='in', width=minor_tick_width, length=minor_tick_length,
                bottom=True, top=True, left=True, right=True)
    
    combined_legend = plt.legend(fontsize=legend_fontsize, loc=2, ncol=1,borderaxespad=1)
    #outline1 = combined_legend.get_frame().set_alpha(0)
    outline = combined_legend.get_frame()
    outline.set_linewidth(legend_boxwidth)
    outline.set_edgecolor('black')
    
    output_dir = os.getcwd()
    file_name = f"thermodynamic_integration.jpg"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')
    
    # output_dir = os.getcwd()
    # file_name = f"Etotal.pdf"
    # file_path = os.path.join(output_dir, file_name)
    # fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    # fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')