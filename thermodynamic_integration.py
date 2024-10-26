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

file_path     = "TP_0.05/TP_B2.dat"
dudl          = np.loadtxt(file_path, skiprows=1, usecols=(0, 1, 2, 3))

file_path_1   = "TP_0.2/TP_B2.dat"
dudl_1        = np.loadtxt(file_path_1, skiprows=1, usecols=(0, 1, 2, 3))

file_path_2   = "TP_0.4/TP_B2.dat"
dudl_2        = np.loadtxt(file_path_2, skiprows=1, usecols=(0, 1, 2, 3))

file_path_3   = "TP_0.6/TP_B2.dat"
dudl_3        = np.loadtxt(file_path_3, skiprows=1, usecols=(0, 1, 2, 3))

file_path_4     = "TP_0.10/TP_B2.dat"
dudl_4          = np.loadtxt(file_path_4, skiprows=1, usecols=(0, 1, 2, 3))

file_path_5     = "TP_0.15/TP_B2.dat"
dudl_5          = np.loadtxt(file_path_5, skiprows=1, usecols=(0, 1, 2, 3))

file_path_6     = "TP_0.02/TP_B2.dat"
dudl_6          = np.loadtxt(file_path_6, skiprows=1, usecols=(0, 1, 2, 3))

# lambda_values = dudl[0:,0]
# du_dlambda_values = dudl[0:,3]
# spline = CubicSpline(lambda_values, du_dlambda_values)
# lambda_fine = np.linspace(0, 1, 1000)
# du_dlambda_fine = spline(lambda_fine)
# area_trapezoid = trapezoid(du_dlambda_fine, lambda_fine)
# # area_trapezoid = trapezoid(du_dlambda_values, lambda_values)
# print("Excess Free Energy for Rho = 0.05 (using trapezoidal rule):", area_trapezoid)

# Calculate and print excess free energy for each dataset
datasets = [dudl_6, dudl, dudl_4, dudl_5, dudl_1, dudl_2, dudl_3]
rhos = [0.02, 0.05, 0.10, 0.15, 0.2, 0.4, 0.6]

for i, data in enumerate(datasets):
    area_trapezoid = calculate_excess_free_energy(data)
    print(f"Excess Free Energy for Rho = {rhos[i]} (using trapezoidal rule):", area_trapezoid)

with plt.style.context([ 'ieee']):
    plt.rcParams['font.family'] = graphic_font
    plt.rcParams['mathtext.fontset'] = math_font
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize=plot_size)
    ax.spines['top'].set_linewidth(spine_width)    
    ax.spines['bottom'].set_linewidth(spine_width) 
    ax.spines['left'].set_linewidth(spine_width)   
    ax.spines['right'].set_linewidth(spine_width)  
    
    dudl_plot_1    = plt.plot(dudl[0:,0], dudl[0:,3],
                    linestyle= 'solid',
                    marker='s',
                    markersize=markersize,
                    color='cyan',
                    label='$\\rho$ = 0.05')
    
    dudl_plot_1    = plt.plot(dudl_4[0:,0], dudl_4[0:,3],
                    linestyle= 'solid',
                    marker='s',
                    markersize=markersize,
                    color='magenta',
                    label='$\\rho$ = 0.1')
    
    dudl_plot_1 = plt.plot(dudl_1[0:,0], dudl_1[0:,3],
                    linestyle= 'solid',
                    marker='s',
                    markersize=markersize,
                    color=MIX_color,
                    label='$\\rho$ = 0.2')
    
    dudl_plot_1 = plt.plot(dudl_2[0:,0], dudl_2[0:,3],
                    linestyle= 'solid',
                    marker='s',
                    markersize=markersize,
                    color='red',
                    label='$\\rho$ = 0.4')

    dudl_plot_1 = plt.plot(dudl_3[0:,0], dudl_3[0:,3],
                    linestyle= 'solid',
                    marker='s',
                    markersize=markersize,
                    color='blue',
                    label='$\\rho$ = 0.6')
    
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
    file_name = f"thermodynamic_integration_A2.jpg"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')
    
    # output_dir = os.getcwd()
    # file_name = f"Etotal.pdf"
    # file_path = os.path.join(output_dir, file_name)
    # fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    # fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')