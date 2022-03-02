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
    plates = [protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", slot)
            for slot in [2, 3, 5, 6, 9]]
    
    #Add Master Mix
    p20Single.transfer(18, mm, pcrWells, new_tip = "once")
    
    #Add culture
    def transfer_culture(strain, dst):
        plate = plates[strain[0]-1]
        p20Single.transfer(1, plate[strain[1]], dst)

    for strain, well in zip(strains, pcrWells):
        transfer_culture(strain, well)
    
    #Add 2nd primer
    for x in range(len(strains)):
        p20Single.transfer(1, alumin.wells()[x], pcrWells[x])
    
    
    