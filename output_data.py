import math
import pandas as pd

def Calculate_Layout_outputs(s1, s2, live_load, column_size, structure_type, length, width,b_s1_mm, d_s1_mm,b_s2_mm, d_s2_mm, slab_thickness):
    building_height = 6
    
    file_name = "productivity_list.csv"
    df = pd.read_csv(file_name)

    if structure_type == "CIS Beam + CIS Slab + CIS Column":
    
        no_s1 = (length/s1) * ((width/s2) + 1)
        no_s2 = ((length/s1)+1) * ((width/s2))
        no_column = ((length/s1)+1) * ((width/s2) + 1)
        
    # Assign values to design data
        no_volumetric_pc_com = 0
        no_vertical_pc_com = 0
        no_propped_slabs = 4
        no_unpropped_slabs = 0
        formwork_area_beams = (no_s1*s1*((b_s1_mm/1000)+1)) + (no_s2*s2*((b_s2_mm/1000)+1))
        formwork_area_slabs = length * width - (formwork_area_beams/2)
        no_column_formworks = no_column
        weight_beam_rebar = math.ceil(((no_s1 * (b_s1_mm/1000) * (d_s1_mm/1000) * s1) + (no_s2 * (b_s2_mm/1000) * (d_s2_mm/1000) * s2)) * 0.353) #(factor rc to rebar 3% tones)
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness) * 0.235) #(factor rc to rebar 2% tones)
        cis_volume = math.ceil((no_s1 * (b_s1_mm/1000) * (d_s1_mm/1000) * s1) + ((no_s2 * (b_s2_mm/1000) * (d_s2_mm/1000) * s2)) + (no_column * column_size * column_size * building_height) + (formwork_area_slabs * slab_thickness))

        # assign values to equipment data
        if length <= 30:
            no_tower_cranes = 1
        elif 30 < length <= 70:
            no_tower_cranes = 2
        elif 70 < length <= 100:
            no_tower_cranes = 3
        
        no_concrete_pumps = 1
        no_passenger_material_hoists = 1
        no_construction_hoists = 0
        no_gondolas = 0
        no_mewps = 0

        # assign values to utility data
        hoist_count_passenger_material = 0
        hoist_count_tower_crane = math.ceil((no_column * 2) + (weight_beam_rebar+weight_slab_rebar)/15 + (formwork_area_beams + formwork_area_slabs)/36)
        no_concrete_truck_deliveries = math.ceil(cis_volume / 8.5)
        no_trailer_deliveries = math.ceil((no_column / 5) + (weight_beam_rebar+weight_slab_rebar)/15)

        beam_manhours = math.ceil(weight_beam_rebar * df.loc[df['category'] == "loosebar_ton", 'manhour'].iloc[0] + formwork_area_beams /16 * df.loc[df['category'] == "vertical_beamfw_pc", 'manhour'].iloc[0] + formwork_area_beams * building_height * 0.5 * df.loc[df['category'] == "scaffold_m3", 'manhour'].iloc[0])
        slab_manhours = math.ceil(weight_slab_rebar * df.loc[df['category'] == "mesh_ton", 'manhour'].iloc[0] + formwork_area_slabs / 16 * df.loc[df['category'] == "vertical_nonrc_pc", 'manhour'].iloc[0] + formwork_area_slabs * building_height * 0.5 * df.loc[df['category'] == "scaffold_m3", 'manhour'].iloc[0])
        column_manhours = math.ceil(no_column * df.loc[df['category'] == "vertical_nonrc_pc", 'manhour'].iloc[0] * 2)
        casting_manhours = math.ceil(cis_volume * df.loc[df['category'] == "casting_pump_m3", 'manhour'].iloc[0])

        # assign values to manpower data
        total_mandays_crane = ((beam_manhours + slab_manhours + column_manhours + casting_manhours)*1.3 +240 + 1800)/ 8 #weather 1.1 manday 8hr safety 1.1 staircase 240 ramp 1400
        total_productivity_crane = ( (length * width) +600) / total_mandays_crane # ramp 600m2

    
        # Design Outputs
        design_output = [
        round(no_volumetric_pc_com),
        round(no_vertical_pc_com),
        round(no_propped_slabs),
        round(no_unpropped_slabs),
        round(formwork_area_slabs),
        round(formwork_area_beams),
        round(no_column_formworks),
        round(weight_beam_rebar),
        round(weight_slab_rebar),
        round(cis_volume)
        ]

        # Equipment Outputs
        equipment_output = [
        round(no_tower_cranes),
        round(no_concrete_pumps),
        round(no_construction_hoists),
        round(no_passenger_material_hoists),
        round(no_gondolas),
        round(no_mewps)
        ]

        # Utility Outputs
        utility_output = [
        round(hoist_count_passenger_material),
        round(hoist_count_tower_crane),
        round(no_concrete_truck_deliveries),
        round(no_trailer_deliveries)
        ]

     # Manpower Outputs
        manpower_output = [
        round(total_mandays_crane),
        round(total_productivity_crane,3),
        round(total_productivity_crane/2,3)
        ]

    return design_output,equipment_output,utility_output,manpower_output, beam_manhours, column_manhours, slab_manhours, casting_manhours
