strains = [[1, 'F7'], [3, 'G5'], [3, 'G7'], [4, 'B7'], [5, 'D8'], [3, 'B3'], [3, 'E9'], [2, 'C3'], [4, 'G3'], [3, 'E7']]

metadata = {
    'protocolName': 'KeioCheck PCR',
    'author': 'Lachlan Munro',
    'source': 'Protocol Library',
    'apiLevel': '2.8'
    }

lowEvapWell = [x + i for x in range(18, 75, 8) for i in (range(4))]

def run(protocol):
    # Load Tips
    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', 1)]

    # Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)

    
    #Load thermocycler
    
    tc_mod = protocol.load_module('thermocycler')
    pcr = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', label="Thermocylcer")
    
    # Load temp_block
    temp_block = protocol.load_module("tempdeck", 4)
    temp_block.set_temperature(4)
    
    alumin = temp_block.load_labware("opentrons_24_aluminumblock_generic_2ml_screwcap")
    
    mm = alumin["D6"]
    
    pcrWells = [pcr.wells()[i] for i in lowEvapWell[0:len(strains)]]
    
    #Load labware
    plates = [protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", slot)
            for slot in [2, 3, 5, 6, 9]]
    
    #Add Master Mix
    p20Single.transfer(18, mm, pcrWells, new_tip = "once", touch_tip=True)
    
    #Add culture
    def transfer_culture(strain, dst):
        plate = plates[strain[0]-1]
        p20Single.transfer(1, plate[strain[1]], dst, mix_after=(1, 20), mix_before=(1, 20))

    for strain, well in zip(strains, pcrWells):
        transfer_culture(strain, well)
    
    #Add 2nd primer
    for x in range(len(strains)):
        p20Single.transfer(1, alumin.wells()[x], pcrWells[x], 
                           mix_after=(1, 20), 
                           mix_before=(1, 20),
                           touch_tip=True)
    
    
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(98)
    #Set initial denaturing
    init_temp = 98
    init_time = 30 
    #set Denaturing
    d_temp = 94
    d_time = 30
    #Set annealing
    a_temp = 52
    a_time = 20
    #Set Extension
    e_temp = 68
    e_time = 45
    
    # Initial denaturing
    tc_mod.set_block_temperature(init_temp, hold_time_seconds=init_time, block_max_volume=25)
                                 
    #Set Profile
    profile = [
        {'temperature': d_temp, 'hold_time_seconds': d_time},
        {'temperature': a_temp, 'hold_time_seconds': a_time},
        {'temperature': e_temp, 'hold_time_seconds': e_time}
    ]

    tc_mod.execute_profile(steps=profile, repetitions=30, block_max_volume=20)

    #Final extension
    tc_mod.set_block_temperature(72, hold_time_seconds = 600, block_max_volume=20)

    tc_mod.set_block_temperature(4)

    
    