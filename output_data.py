import math
import pandas as pd

def calculate_layout_outputs(s1, s2, live_load, column_size_mm, selected_column, selected_beam, selected_slab, length, width, b_s1_mm, d_s1_mm,b_s2_mm, d_s2_mm, b_s3_mm, d_s3_mm,slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm):
    building_height = 6
    

    # Initialize all return-related variables to default values
    no_volumetric_pc_com = 0
    no_vertical_pc_com = 0
    no_propped_slabs = 0
    no_unpropped_slabs = 0
    formwork_area_slabs = 0
    formwork_area_beams = 0
    no_column_formworks = 0
    weight_loose_rebar = 0
    weight_slab_rebar = 0
    cis_volume = 0
    no_tower_cranes = 0
    no_concrete_pumps = 1
    no_construction_hoists = 0
    no_passenger_material_hoists = 1
    no_gondolas = 0
    no_mewps = 0
    hoist_count_passenger_material = 0
    hoist_count_tower_crane = 0
    no_concrete_truck_deliveries = 0
    no_trailer_deliveries = 0
    beam_manhours = 0
    slab_manhours = 0
    column_manhours = 0
    casting_manhours = 0
    total_mandays_crane = 0
    total_productivity_crane = 0
    slab_cis_volume = 0
    beam_cis_volume = 0
    column_cis_volume = 0
    weight_beam_rebar = 0
    weight_column_rebar = 0
    weight_slab_rebar = 0
    weight_loose_rebar = 0
    beam_hoist_count_tower_crane = 0
    slab_hoist_count_tower_crane = 0
    column_hoist_count_tower_crane = 0

    file_name = "productivity_list.csv"
    df = pd.read_csv(file_name)
    
    # Export manhour values for each category
    manhour_vertical_nonrc_pc = df.loc[df['category'] == "vertical_nonrc_pc", 'manhour'].iloc[0]
    manhour_vertical_beamfw_pc = df.loc[df['category'] == "vertical_beamfw_pc", 'manhour'].iloc[0]
    manhour_casting_pump_m3 = df.loc[df['category'] == "casting_pump_m3", 'manhour'].iloc[0]
    manhour_loosebar_ton = df.loc[df['category'] == "loosebar_ton", 'manhour'].iloc[0]
    manhour_mesh_ton = df.loc[df['category'] == "mesh_ton", 'manhour'].iloc[0]
    manhour_scaffold_m3 = df.loc[df['category'] == "scaffold_m3", 'manhour'].iloc[0]
    manhour_posttension_pc = df.loc[df['category'] == "posttension_pc", 'manhour'].iloc[0]
    
    no_s1 = (length/s1) * ((width/s2) + 1)
    no_s2 = ((length/s1) + 1) * ((width/s2))
    no_s3 = (length/s1) * (((width/s2) + 1)-1)
    no_column = ((length/s1) + 1) * ((width/s2) + 1)
    
    b_s1_m = b_s1_mm / 1000
    d_s1_m = d_s1_mm / 1000
    b_s2_m = b_s2_mm / 1000
    d_s2_m = d_s2_mm / 1000
    b_s3_m = b_s3_mm / 1000
    d_s3_m = d_s3_mm / 1000
    slab_thickness_m = slab_thickness_mm/1000
    column_size_m = column_size_mm
    
    # assign values to equipment data
    if length <= 30:
        no_tower_cranes = 1
    elif 30 < length <= 70:
        no_tower_cranes = 2
    elif 70 < length <= 100:
        no_tower_cranes = 3
    

    
    if (selected_beam == "CIS Beam"):
        formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1))
        beam_rebar_percentage = 3
        weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
        beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2))

        beam_manhours = math.ceil(weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc
        
        beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /8) 
        
    if (selected_beam == "PT Beam"):
        formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1))
        beam_rebar_percentage = 4
        weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
        beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2))
        total_no_pt_tendon = int(length / s1 + 1 + width / s2 + 1)
                
        beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /18) 
        
        beam_manhours = math.ceil(total_no_pt_tendon * manhour_posttension_pc + weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc

        
    if (selected_column == "CIS Column"):
        no_column_formworks = no_column
        column_cis_volume = math.ceil((no_column * column_size_m * column_size_m * building_height))
        column_rebar_percentage = 2
        weight_column_rebar = math.ceil((no_column * column_size_m * column_size_m * building_height) * 7.85 * column_rebar_percentage/100) #7.85 density rebar
        
        column_manhours = math.ceil(no_column * manhour_vertical_nonrc_pc + weight_column_rebar * manhour_loosebar_ton + column_cis_volume)
        
        column_hoist_count_tower_crane = math.ceil(no_column + weight_column_rebar/6) 
        
    if (selected_column == "PC Column"):
        no_vertical_pc_com = no_column
        column_cis_volume = math.ceil((no_column * column_size_m * column_size_m * building_height))
        column_rebar_percentage = 2
        weight_column_rebar = math.ceil((no_column * column_size_m * column_size_m * building_height) * 7.85 * column_rebar_percentage/100) #7.85 density rebar
        
        column_manhours = math.ceil(no_column * manhour_vertical_nonrc_pc)
        
        column_hoist_count_tower_crane = math.ceil(no_column) 
    
    if (selected_slab == "CIS Slab"):
        formwork_area_slabs = length * width - (formwork_area_beams / 2)
        slab_rebar_percentage = 1.5
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = formwork_area_slabs * slab_thickness_m
        
        slab_manhours = math.ceil(weight_slab_rebar * manhour_mesh_ton + formwork_area_slabs / 16 * manhour_vertical_beamfw_pc + formwork_area_slabs * building_height * 0.5 * manhour_scaffold_m3) #5 storey scaffold install about 2.5floors

        slab_hoist_count_tower_crane = math.ceil(weight_slab_rebar /4 + formwork_area_slabs/16) 
        
    if (selected_slab == "PT Flat Slab"):
        formwork_area_slabs = length * width
        slab_rebar_percentage = 4
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = formwork_area_slabs * slab_thickness_m
        
        # Calculate tendon spacing (use the average of 6h to 8h)
        tendon_spacing = 6 * slab_thickness_m  # Average spacing in meters

        # Number of tendons in each direction
        no_pt_tendon_x = math.ceil(length / tendon_spacing)  # Tendons in x-direction
        no_pt_tendon_y = math.ceil(width / tendon_spacing)   # Tendons in y-direction

        # Total tendons
        total_no_pt_tendon = no_pt_tendon_x + no_pt_tendon_y 
        
        slab_manhours = math.ceil(total_no_pt_tendon * manhour_posttension_pc + weight_slab_rebar * manhour_mesh_ton + formwork_area_slabs * building_height * 0.5 * manhour_scaffold_m3) #5 storey scaffold install about 2.5floors
    
        slab_hoist_count_tower_crane = math.ceil(weight_slab_rebar /4 + formwork_area_slabs/16) 
    
    if (selected_slab == "1.2HC Slab"):
        topping_area_slabs = length * width - (formwork_area_beams / 2)
        formwork_area_slabs = 0
        slab_rebar_percentage = 1.5
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = topping_area_slabs * slab_thickness_m
        
        # Calculate the number of x positions
        N_x = int(length / s1)

        # Calculate the number of y positions
        N_y = int(width/ s2)

        # Calculate the number of stacked rectangles per position
        N_stacked = int((s2 -column_size_mm) / 1.2)

        # Calculate the total number of 1.2HCS
        no_unpropped_slabs = int(N_x * N_y * N_stacked)
 
        slab_manhours = math.ceil(weight_slab_rebar * manhour_mesh_ton + no_unpropped_slabs * manhour_vertical_nonrc_pc) #prepare topping + hoisting
    
        slab_hoist_count_tower_crane = math.ceil(no_unpropped_slabs + weight_slab_rebar/4) 
    
    if (selected_slab == "2.4HC Slab"):
        topping_area_slabs = length * width - (formwork_area_beams / 2)
        formwork_area_slabs = 0
        slab_rebar_percentage = 1.5
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = topping_area_slabs * slab_thickness_m
        
        # Calculate the number of x positions
        N_x = int((length + s1 - (s1 * 1.5)) / s1)

        # Calculate the number of y positions
        N_y = int((width + s2 - (s2 + 2 * column_size_mm)) / s2)

        # Calculate the number of stacked rectangles per position
        N_stacked = math.floor((s2 -column_size_mm) / 2.4)

        # Calculate the total number of 2.4HCS
        no_unpropped_slabs = int(N_x * N_y * N_stacked)
 
        slab_manhours = math.ceil(weight_slab_rebar * manhour_mesh_ton + no_unpropped_slabs * manhour_vertical_nonrc_pc) #prepare topping + hoisting
    
        slab_hoist_count_tower_crane = math.ceil(no_unpropped_slabs + weight_slab_rebar/4) 
        
    if (selected_slab == "1.2HCS_S3"):
        topping_area_slabs = length * width - (formwork_area_beams / 2)
        formwork_area_slabs = 0
        slab_rebar_percentage = 1.5
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = topping_area_slabs * slab_thickness_m
        
        # Calculate the number of x positions
        N_x = int(length / (s1/2))

        # Calculate the number of y positions
        N_y = int(width/ s2)

        # Calculate the number of stacked rectangles per position
        N_stacked = int((s2 -column_size_mm) / 1.2)

        # Calculate the total number of 1.2HCS
        no_unpropped_slabs = int(N_x * N_y * N_stacked)

        slab_manhours = math.ceil(weight_slab_rebar * manhour_mesh_ton + no_unpropped_slabs * manhour_vertical_nonrc_pc) #prepare topping + hoisting

        slab_hoist_count_tower_crane = math.ceil(no_unpropped_slabs + weight_slab_rebar/4) 
        
        
        if (selected_beam == "CIS Beam"):
            formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1)) + (no_s3 * s1 * (b_s3_m + 1))
            beam_rebar_percentage = 3
            weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
            beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1))

            beam_manhours = math.ceil(weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc
            
            beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /8) 
            
        if (selected_beam == "PT Beam"):
            formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1)) + (no_s3 * s1 * (b_s3_m + 1))
            beam_rebar_percentage = 4
            weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
            beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1))
            total_no_pt_tendon = int(length / s1 + 1 + width / s2 + 1)
                    
            beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /18) 
            
            beam_manhours = math.ceil(total_no_pt_tendon * manhour_posttension_pc + weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc

    if (selected_slab == "2.4HCS_S3"):
        topping_area_slabs = length * width - (formwork_area_beams / 2)
        formwork_area_slabs = 0
        slab_rebar_percentage = 1.5
        weight_slab_rebar = math.ceil((formwork_area_slabs * slab_thickness_m) * 7.85 * slab_rebar_percentage/100)
        slab_cis_volume = topping_area_slabs * slab_thickness_m
        
        # Calculate the number of x positions
        N_x = int(length / (s1/2))

        # Calculate the number of y positions
        N_y = int(width/ s2)

        # Calculate the number of stacked rectangles per position
        N_stacked = int((s2 -column_size_mm) / 2.4)

        # Calculate the total number of 1.2HCS
        no_unpropped_slabs = int(N_x * N_y * N_stacked)

        slab_manhours = math.ceil(weight_slab_rebar * manhour_mesh_ton + no_unpropped_slabs * manhour_vertical_nonrc_pc) #prepare topping + hoisting

        slab_hoist_count_tower_crane = math.ceil(no_unpropped_slabs + weight_slab_rebar/4) 
        
        if (selected_beam == "CIS Beam"):
            formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1)) + (no_s3 * s1 * (b_s3_m + 1))
            beam_rebar_percentage = 3
            weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
            beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1))

            beam_manhours = math.ceil(weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc
            
            beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /8) 
        
        if (selected_beam == "PT Beam"):
            formwork_area_beams = (no_s1 * s1 * (b_s1_m + 1)) + (no_s2 * s2 * (b_s2_m + 1)) + (no_s3 * s1 * (b_s3_m + 1))
            beam_rebar_percentage = 4
            weight_beam_rebar = math.ceil(((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1)) * 7.85 * beam_rebar_percentage/100) #7.85 density rebar
            beam_cis_volume = math.ceil((no_s1 * b_s1_m * d_s1_m * s1) + (no_s2 * b_s2_m * d_s2_m * s2) + (no_s3 * b_s3_m * d_s3_m * s1))
            total_no_pt_tendon = int(length / s1 + 1 + width / s2 + 1)
                
        beam_hoist_count_tower_crane = math.ceil(weight_beam_rebar/4 + formwork_area_beams /18) 
        
        beam_manhours = math.ceil(total_no_pt_tendon * manhour_posttension_pc + weight_beam_rebar * manhour_loosebar_ton + formwork_area_beams /8 * manhour_vertical_beamfw_pc + formwork_area_beams * building_height * 0.5 * manhour_scaffold_m3) #horizontal formwork 16m2 a pc

        
    
    no_propped_slabs = no_propped_slabs + 8
    weight_loose_rebar = weight_column_rebar + weight_beam_rebar
    cis_volume = beam_cis_volume + column_cis_volume + slab_cis_volume
    
    casting_manhours = math.ceil(cis_volume * manhour_casting_pump_m3)
    
    # assign values to utility data
    hoist_count_passenger_material = 0
    hoist_count_tower_crane = column_hoist_count_tower_crane + slab_hoist_count_tower_crane + beam_hoist_count_tower_crane
    no_concrete_truck_deliveries = math.ceil(cis_volume / 8.5)
    no_trailer_deliveries = math.ceil((no_vertical_pc_com + no_propped_slabs + no_unpropped_slabs)/5 + (weight_beam_rebar + weight_slab_rebar + weight_column_rebar)/15)
    
    # assign values to manpower data
    total_mandays_crane = ((beam_manhours + slab_manhours + column_manhours + casting_manhours)*1.3 +240)/ 8 #weather 1.1 manday 8hr safety 1.1 staircase 240 ramp 1400
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
    round(weight_loose_rebar),
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
    round(1.3*0.6*hoist_count_tower_crane/no_tower_cranes/8,2), #1.3 weather, /8 for manhours, 0.6 meaning 40minutes a hoist
    round(total_mandays_crane/(1.3*hoist_count_tower_crane*0.8/no_tower_cranes/8))
    ]
    
    # All Outputs for verification
    misc_output = [
        no_volumetric_pc_com,
        no_vertical_pc_com,
        no_propped_slabs,
        no_unpropped_slabs,
        formwork_area_slabs,
        formwork_area_beams,
        no_column_formworks,
        weight_loose_rebar,
        weight_slab_rebar,
        cis_volume,
        no_tower_cranes,
        no_concrete_pumps,
        no_construction_hoists,
        no_passenger_material_hoists,
        no_gondolas,
        no_mewps,
        hoist_count_passenger_material,
        hoist_count_tower_crane,
        no_concrete_truck_deliveries,
        no_trailer_deliveries,
        beam_manhours,
        slab_manhours,
        column_manhours,
        casting_manhours,
        total_mandays_crane,
        total_productivity_crane,
        slab_cis_volume,
        beam_cis_volume,
        column_cis_volume,
        weight_beam_rebar,
        weight_column_rebar,
        weight_slab_rebar,
        weight_loose_rebar,
        beam_hoist_count_tower_crane,
        slab_hoist_count_tower_crane,
        column_hoist_count_tower_crane
    ]


    return misc_output, design_output,equipment_output,utility_output,manpower_output, beam_manhours, column_manhours, slab_manhours, casting_manhours
