import math
import pandas as pd

def calculate_slab_thickness(s1, s2, live_load, selected_slab):
    """
    Calculate the slab thickness and associated parameters based on the type of slab.
    
    Parameters:
    - s1 (float): Span of the slab in meters.
    - s2 (float): Secondary span of the slab in meters.
    - live_load (float): Live load in kN/m².
    - selected_slab (str): Type of slab ("CIS Slab", "PT Flat Slab", "1.2HC Slab", "2.4HC Slab").
    
    Returns:
    - slab_thickness_mm (float): Recommended slab thickness in mm.
    - slab_max_spacing_pt_mm (float): Maximum tendon spacing in mm (for PT slabs only).
    - hcs_weight_tonnes (float): Weight of hollow core slab in tonnes (for HCS slabs only).
    """
    # Initialize default values
    slab_thickness_mm = None
    slab_max_spacing_pt_mm = None
    hcs_weight_tonnes = None

    file_name_hcs = "hcs_data.csv"
    hcsdata = pd.read_csv(file_name_hcs)

    if selected_slab == "CIS Slab":
        # Step 1: Set parameters
        R_max = 25  # Base ratio for the lightest load
        L_ref = 3   # Reference live load (kPa)
        k = 0.25    # Sensitivity factor for live load
        n = 0.2     # Sensitivity factor for span length

        R_base = R_max * (L_ref / live_load)**k
        R_adjusted = R_base * (10 / s1)**n

        effective_depth = s1 / R_adjusted
        nominal_cover = 0.03
        bar_diameter = 0.016
        slab_thickness = effective_depth + nominal_cover + bar_diameter
        minimum_thickness = 0.15
        slab_thickness = max(slab_thickness, minimum_thickness)
        slab_thickness_mm = math.floor(slab_thickness * 1000 / 50) * 50
        
        hcs_slab_thickness_mm = 0
        slab_max_spacing_pt_mm = 0

    elif selected_slab == "PT Flat Slab":
        if live_load <= 3:
            span_to_depth_ratio = 45
        elif 3 < live_load <= 5:
            span_to_depth_ratio = 40
        elif 5 < live_load <= 15:
            span_to_depth_ratio = 35
        elif 15 < live_load <= 25:
            span_to_depth_ratio = 30
        else:
            span_to_depth_ratio = 25

        effective_depth = s1 / span_to_depth_ratio
        nominal_cover = 0.03
        pt_duct_space = 0.02
        slab_thickness = effective_depth + nominal_cover + pt_duct_space
        minimum_thickness = 0.2
        slab_thickness = max(slab_thickness, minimum_thickness)
        slab_thickness_mm = math.ceil(slab_thickness * 1000 / 50) * 50

        total_prestressing_force = 1.5 * live_load * s1 * s2
        strand_capacity = 300
        num_tendons = math.ceil(total_prestressing_force / (strand_capacity * 4))
        slab_max_spacing_pt_mm = min(8 * slab_thickness * 1000, s1 * 1000 / num_tendons)
        slab_max_spacing_pt_mm = math.floor(slab_max_spacing_pt_mm / 50) * 50
        
        hcs_slab_thickness_mm = 0

    elif selected_slab in ["1.2HC Slab", "2.4HC Slab"]:
        # Filter data to find slabs that meet or exceed the given span and live load
        filtered_data = hcsdata[(hcsdata['span'] >= s1) & (hcsdata['hcs_load_capacity'] >= live_load)]

        if not filtered_data.empty:
            # Find the minimum slab thickness
            hcs_slab_thickness_mm = filtered_data['hcs_thickness'].min()
        else:
            raise ValueError("No matching slabs found for the given span and live load.")
            
        slab_thickness_mm = 75
        slab_max_spacing_pt_mm = 0

    elif hcs_slab_thickness_mm is None:
        hcs_slab_thickness_mm = 0
    
    return slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm
