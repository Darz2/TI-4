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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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

########################### Loading plot data ############################
file_path_radial   = 'Radial_100'
radial             = np.loadtxt(file_path_radial, skiprows=1)
# print(radial[0:,0])

with plt.style.context([ 'ieee']):
    plt.rcParams['font.family'] = graphic_font
    plt.rcParams['mathtext.fontset'] = math_font
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize=plot_size)
    ax.spines['top'].set_linewidth(spine_width)    
    ax.spines['bottom'].set_linewidth(spine_width) 
    ax.spines['left'].set_linewidth(spine_width)   
    ax.spines['right'].set_linewidth(spine_width)  
    
    radial_plot_1 = plt.plot(radial[0:,0], radial[0:,1],
                    linestyle= 'solid',
                    color=CO2_color,
                    label="$g(r)$")
    
    radial_plot_2 = plt.plot(radial[0:,0], radial[0:,2],
                    linestyle= 'solid',
                    color=MIX_color,
                    label="$g^{\infty}(r)$")
    
    plt.xlabel(r'$r$', fontsize=label_fontsize)
    plt.ylabel(r'RDF',fontsize=label_fontsize)
    
    plt.xlim(-0.25, 5)
    plt.ylim(-0.05, 1.39)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    
    # plt.xlim(0.5, 2)
    # plt.ylim(0.8, 1.39)
    
    ax.tick_params(axis='both', which='major', direction='in', width=tick_width, length=tick_length, labelsize=tick_labelsize,
                bottom=True, top=True, left=True, right=True)
    ax.tick_params(axis='both', which='minor', direction='in', width=minor_tick_width, length=minor_tick_length,
                bottom=True, top=True, left=True, right=True)
    
    combined_legend = plt.legend(fontsize=legend_fontsize, loc=1, ncol=1,borderaxespad=1)
    #outline1 = combined_legend.get_frame().set_alpha(0)
    outline = combined_legend.get_frame()
    outline.set_linewidth(legend_boxwidth)
    outline.set_edgecolor('black')
    
    # Add an inset axes for zoomed-in view
    ax_inset = inset_axes(plt.gca(), width="40%", height="40%",
                      bbox_to_anchor=(-0.15, 0.15, 1, 1),  # x, y, width, height relative to the main plot
                      bbox_transform=plt.gca().transAxes,  # Transform relative to axes
                      loc='lower right')
    ax_inset.plot(radial[0:,0], radial[0:,1],
                    linestyle= 'solid',
                    color=CO2_color)
    ax_inset.plot(radial[0:,0], radial[0:,2],
                    linestyle= 'solid',
                    color=MIX_color)
    
    ax_inset.axhline(1, color="black", linewidth=0.5, linestyle='--')
    
    # Zoom-in region
    x_min, x_max = 0.9, 2.05  
    y_min, y_max = 0.95, 1.35
    ax_inset.set_xlim(x_min, x_max)
    ax_inset.set_ylim(y_min, y_max)
    
    ax_inset.xaxis.set_major_locator(MultipleLocator(0.5))
    ax_inset.xaxis.set_minor_locator(MultipleLocator(0.25))
    ax_inset.yaxis.set_major_locator(MultipleLocator(0.2))
    ax_inset.yaxis.set_minor_locator(MultipleLocator(0.1))

    ax_inset.tick_params(axis='both', which='major', direction='in',
                bottom=True, top=True, left=True, zorder=2, right=True)
    ax_inset.tick_params(axis='both', which='minor', direction='in',
                bottom=True, top=True, left=True,zorder=2, right=True)    
    
    output_dir = os.getcwd()
    file_name = f"radial_N_100_Rho_0.01_L_1.00_B_1_S_1.jpg"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')
    
    output_dir = os.getcwd()
    file_name = f"Figure7a.pdf"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')