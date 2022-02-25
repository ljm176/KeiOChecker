# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:01:39 2022

@author: lajamu
"""

from find_strain_positions import list_positions
import openpyxl

        
strainswb = openpyxl.load_workbook("keioPrimers1.xlsx")
strainsSheet = strainswb.active
genes = []
for row in range(2, strainsSheet.max_row +1):
        genes.append(strainsSheet["A" + str(row)].value)

print(list_positions(genes))
