# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:01:39 2022

@author: lajamu
"""

from find_strain_positions import list_positions
import openpyxl

def write_pcr_file(fileName):
    strainswb = openpyxl.load_workbook(fileName)
    strainsSheet = strainswb.active
    genes = []
    for row in range(2, strainsSheet.max_row +1):
            genes.append(strainsSheet["A" + str(row)].value)
    
    #print(list_positions(genes))
    
    pcrProt = open("Templates/pcr_protocol_txt.txt", "r")
    new_pcrProt_name = fileName[:-5] + "OT_Protocol.py"
    
    new_pcrProt = open(new_pcrProt_name, "w")
    
    new_pcrProt.write("strains = " + str(list_positions(genes)))
    new_pcrProt.write("\n")
    new_pcrProt.write("\n")
    
    for line in pcrProt:
        new_pcrProt.write(line)
    new_pcrProt.close()
    print("PCR Protocol generation Complete")
    return(new_pcrProt_name)