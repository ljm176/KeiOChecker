# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 07:12:42 2022

@author: lajamu
"""

from make_primer import write_primer_to_xl
from write_pcr_protocol import write_pcr_file
import os, shutil

def write_protocol_and_primers(filename):
    dirname = filename[:-5]
    if dirname not in os.listdir():
        os.mkdir(dirname)
    primerFile = write_primer_to_xl(filename)
    protocolFile = write_pcr_file(filename)
    
    shutil.move(primerFile, dirname)
    shutil.move(protocolFile, dirname)

write_protocol_and_primers("keioPrimers1.xlsx")
    
