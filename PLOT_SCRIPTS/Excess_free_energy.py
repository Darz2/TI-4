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

markers = ['o', 's', '^', 'D', 'h', '*', 'X' , "8"]
plot_size = (4, 3)
graphic_font = 'Arial'
math_font = 'dejavuserif'  #['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']
spine_width = 1
markersize=4
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
label_fontsize=12
borderaxespad=0.6
alpha = 1
CO2_color = '#e41a1c'
MIX_color = '#008000'
TI_color = '#0000FF'
rgba_CO2_color = mcolors.to_rgba(CO2_color)
rgba_MIX_color = mcolors.to_rgba(MIX_color)
rgba_TI_color = mcolors.to_rgba(TI_color)
CO2_face_color = (rgba_CO2_color[0], rgba_CO2_color[1], rgba_CO2_color[2], 0.6)
MIX_face_color = (rgba_MIX_color[0], rgba_MIX_color[1], rgba_MIX_color[2], 0.6)
TI_face_color = (rgba_TI_color[0], rgba_TI_color[1], rgba_TI_color[2], 0.6)
resolution_value = 1200
break_threshold = 10 # for NIST data
plt.rcParams['font.serif'] = graphic_font
plt.rcParams['mathtext.fontset'] = math_font

file_path_TP   = '../EXCESS_ENTROPY/TP_B2.dat'
TP             = np.loadtxt(file_path_TP, skiprows=1)

file_path_SD   = '../EXCESS_ENTROPY/SD_TP_B2.dat'
SD             = np.loadtxt(file_path_SD, skiprows=1)

'''
EXCESS_ENTROPY/TP_B2.dat

Free Energy incides                                 = 7
Free Energy (with corrected g) incides              = 8
Free Energy (Thermodynamic Integration) incides     = 9

EXCESS_ENTROPY/SD_TP_B2.dat

SD of Free incides  = 6
Free Energy (with corrected g) incides = 7

'''

with plt.style.context([ 'ieee']):
    plt.rcParams['font.family'] = graphic_font
    plt.rcParams['mathtext.fontset'] = math_font
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize=plot_size)
    ax.spines['top'].set_linewidth(spine_width)    
    ax.spines['bottom'].set_linewidth(spine_width) 
    ax.spines['left'].set_linewidth(spine_width)   
    ax.spines['right'].set_linewidth(spine_width) 
    
    Plot_FE  = plt.errorbar(TP[0:,0], TP[0:,7],yerr=SD[0:,6],
                fmt='o',
                markersize=markersize,
                markerfacecolor=CO2_face_color,
                markeredgecolor='k',
                markeredgewidth=markeredgewidth,
                linestyle='solid',
                linewidth= linewidth,
                capsize=capsize,
                capthick=capsize,
                color=CO2_color,
                label='$g(r)$')
    
    Plot_FEC = plt.errorbar(TP[0:,0], TP[0:,8],yerr=SD[0:,7],
                fmt='s',
                markersize=markersize,
                markerfacecolor=MIX_face_color,
                markeredgecolor='k',
                markeredgewidth=markeredgewidth,
                linestyle='solid',
                linewidth= linewidth,
                capsize=capsize,
                capthick=capsize,
                color=MIX_color,
                label='$g^{\infty}(r)$')
    
    Plot_TI  = plt.plot(TP[0:,0], TP[0:,9],
                marker = 'D',
                markersize=markersize,
                markerfacecolor=TI_face_color,
                markeredgecolor='k',
                markeredgewidth=markeredgewidth,
                linestyle='solid',
                linewidth= linewidth,
                color=TI_color,
                label='$\mathrm{TI}$')
    
    plt.xlabel(r'$\rho$', fontsize=label_fontsize)
    plt.ylabel(r'$A^{\mathrm{ex}}/N$',fontsize=label_fontsize)
    
    plt.ylim(-3, 24)
    # plt.xlim(-0.1, 1.1)
    
    ax.set_xscale('log') 
    
    # ax.xaxis.set_major_locator(MultipleLocator(0.2))
    # ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    # ax.yaxis.set_major_locator(MultipleLocator(1))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    
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
    file_name = f"Free_energy.jpg"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')
    
    # output_dir = os.getcwd()
    # file_name = f"Free_energy.pdf"
    # file_path = os.path.join(output_dir, file_name)
    # fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    # fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')