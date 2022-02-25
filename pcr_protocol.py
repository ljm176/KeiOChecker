# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:08:28 2022

@author: lajamu
"""

strains = [[1, 'F7'], [3, 'G5'], [3, 'G7'], [4, 'B7'], [5, 'D8'], [3, 'B3'], 
 [3, 'E9'], [2, 'C3'], [4, 'G3'], [3, 'E7']]

metadata = {
    'protocolName': 'KeioCheck PCR',
    'author': 'Lachlan Munro',
    'source': 'Protocol Library',
    'apiLevel': '2.8'
    }

lowEvapWell = [x + i for x in range(18, 75, 8) for i in (range(4))]

def run(protocol):
    # Load Tips
    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '6')]
    #tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '3')]

    # Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    #p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips300)
    
    #Load thermocycler
    
    tc_mod = protocol.load_module('thermocycler')
    pcr = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', label="Thermocylcer")
    
    # Load temp_block
    temp_block = protocol.load_module("tempdeck", 1)
    temp_block.set_temperature(4)
    
    pcrWells = [pcr.wells()[i] for i in lowEvapWell[0:len(strains)]]
    
    #Load labware
    plates = [protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", slot)
            for slot in [3, 4, 5, 2, 9]]
    
    def transfer_culture(strain, dst):
        plate = plates[strain[0]-1]
        p20Single.transfer(1, plate[strain[1]], dst)
    
    
    
    for strain, well in zip(strains, pcrWells):
        transfer_culture(strain, pcrWells)
    
    
    