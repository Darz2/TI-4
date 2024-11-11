#!/usr/bin/env python

T = 4
N = 500
rc = 2

table_preamble = [
        '%-------TABLE-2------- \n'
        f'%---------T={T}------- \n'
        f'%---------N={N}------- \n'
        f'%---------rc={rc}------- \n'
        '\\begin{table}[tbh!]\n',
        f'\caption{{Computed excess entropy ($S^{{\mathrm{{ex}}}}$) from Thermodynamic Integration (TI) and from Eq.~\\ref{{eq:excess}}, \
            with the finite-size correction for $g(r)$ as proposed by Ganguly and van der Vegt \cite{{ganguly2013convergence}} \
            and without finite-size correction for $g(r)$, for $T= {T}$, $r_c = {rc}$, and $N = {N}$}}\n',
        f'\label{{TAB:1-T={T}}}\n',
        '\centering\n',
        '\\begin{tabular}{P{1cm} P{1.5cm} P{1.5cm} P{2.25cm} P{2.25cm} P{2cm} P{2cm}} \n',
        '\\toprule\n',
        '${ \\rho }$ & {$ U/N $} & {$ S^{\mathrm{ex}}_{\mathrm{TI}}/N $} & {$ S^{\mathrm{ex}}(q_s^{\infty}(r))/N $} & {$ S^{\mathrm{ex}}(q_s(r))/N $} & \
            \parbox{2cm}{APE \\ $S^{\mathrm{ex}}(q_s^{\infty}(r))$} & \parbox{2cm}{APE \\ $S^{\mathrm{ex}}(q_s(r))$} \\\\ \midrule \n'
    ]

#table close
table_close = [
    '\\bottomrule \n'
    '\end{tabular} \n'
    '\end{table}\n'
]
    
TP_filename = f'TP_B2.dat'
SD_TP_filename = f'SD_TP_B2.dat'
ERROR_TP_filename = f'ERROR_TP_B2.dat'
    
    
with open(TP_filename, 'r') as MC_TP, \
     open(SD_TP_filename, 'r') as MC_SD_TP, \
     open(ERROR_TP_filename, 'r') as ERROR_TP:
        
    TP_line         = MC_TP.readlines()
    SD_TP_line      = MC_SD_TP.readlines()
    ERROR_TP_line   = ERROR_TP.readlines()

    output_table_filename = f'LATEX_TABLE_{T}.txt'

    with open(output_table_filename, 'w') as output_file:
        
        output_file.writelines(table_preamble)

        for TP_line, SD_TP_line, ERROR_TP_line in zip(TP_line[2:], SD_TP_line[2:], ERROR_TP_line[2:]):
            
            array_one = TP_line.split()
            array_two = SD_TP_line.split()
            array_three = ERROR_TP_line.split()

            table_1 = f""" {float(array_one[0]):.2f} \
                        & {float(array_one[2]):.4f} \
                        & {float(array_one[7]):.4f} \
                        & {float(array_one[6]):.4f} \
                        & {float(array_one[5]):.4f} \
                        & {float(array_three[8]):.2f} \
                        & {float(array_three[7]):.2f} \\\\ """
                                            
            output_file.write(table_1 + '\n')

        output_file.writelines(table_close)