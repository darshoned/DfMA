import math
import pandas as pd

def hcs_selected_slab_check(s1, live_load, selected_slab):
    # Read HCS data
    file_name_hcs = "hcs_data.csv"
    hcsdata = pd.read_csv(file_name_hcs)
    
    def find_min_hcs_thickness(s1, live_load):
        # Filter HCS data based on span and load capacity
        filtered_data = hcsdata[(hcsdata['s1'] >= s1) & (hcsdata['hcs_load_capacity'] >= live_load)]
        return filtered_data['hcs_thickness'].min() if not filtered_data.empty else None

    # If selected slab is in the given list, return the same value
    if selected_slab in ["CIS Slab", "PT Flat Slab"]:
        return selected_slab

    # For "1.2HC Slab" and "2.4HC Slab", check HCS thickness and possibly update slab type
    if selected_slab == "1.2HC Slab":
        hcs_slab_thickness_mm = find_min_hcs_thickness(s1, live_load)
        if hcs_slab_thickness_mm is None:
            selected_slab = "1.2HCS_S3"  # If no suitable thickness is found, modify the slab selection
        else:
            selected_slab = "1.2HC Slab"  # Keep the same slab if a suitable thickness is found

    
    if selected_slab == "2.4HC Slab":
        hcs_slab_thickness_mm = find_min_hcs_thickness(s1, live_load)
        if hcs_slab_thickness_mm is None:
            selected_slab = "2.4HCS_S3"  # If no suitable thickness is found, modify the slab selection
        else:
            selected_slab = "2.4HC Slab"  # Keep the same slab if a suitable thickness is found

    return selected_slab





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
    - hcs_slab_thickness_mm (float): Thickness of the selected hollow core slab (for HCS slabs only).
    """
    # Initialize default values
    slab_thickness_mm = 0
    slab_max_spacing_pt_mm = 0
    hcs_slab_thickness_mm = 0

    # Read HCS data
    file_name_hcs = "hcs_data.csv"
    hcsdata = pd.read_csv(file_name_hcs)

    if selected_slab == "CIS Slab":
        # Step 1: Set parameters
        R_max = 25  # Base ratio for the lightest load
        L_ref = 3   # Reference live load (kPa)
        k = 0.25    # Sensitivity factor for live load
        n = 0.2     # Sensitivity factor for span length

        R_base = R_max * (L_ref / live_load) ** k
        R_adjusted = R_base * (10 / s1) ** n

        effective_depth = s1 / R_adjusted
        nominal_cover = 0.03
        bar_diameter = 0.016
        slab_thickness = effective_depth + nominal_cover + bar_diameter
        minimum_thickness = 0.15
        slab_thickness = max(slab_thickness, minimum_thickness)
        slab_thickness_mm = math.floor(slab_thickness * 1000 / 50) * 50

        slab_max_spacing_pt_mm = 0

    elif selected_slab == "PT Flat Slab":
        if live_load <= 3:
            span_to_depth_ratio = 45
        elif 3 < live_load <= 5:
            span_to_depth_ratio = 40
        elif 5 < live_load <= 10:
            span_to_depth_ratio = 37
        elif 10 < live_load <= 15:
            span_to_depth_ratio = 33
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
        slab_thickness_mm = math.ceil(slab_thickness * 1000 / 25) * 25

        total_prestressing_force = 1.5 * live_load * s1 * s2
        strand_capacity = 300
        num_tendons = math.ceil(total_prestressing_force / (strand_capacity * 4))
        slab_max_spacing_pt_mm = min(8 * slab_thickness * 1000, s1 * 1000 / num_tendons)
        slab_max_spacing_pt_mm = math.floor(slab_max_spacing_pt_mm / 50) * 50

    elif selected_slab in ["1.2HC Slab", "2.4HC Slab", "1.2HCS_S3", "2.4HCS_S3"]:
        # Function to find minimum thickness for a given span
        def find_min_hcs_thickness(s1, live_load):
            filtered_data = hcsdata[(hcsdata['s1'] >= s1) & (hcsdata['hcs_load_capacity'] >= live_load)]
            return filtered_data['hcs_thickness'].min() if not filtered_data.empty else None

        # First attempt with full span s1
        hcs_slab_thickness_mm = find_min_hcs_thickness(s1, live_load)

        # If no suitable slab is found, retry with s1/2
        if hcs_slab_thickness_mm is None:
            hcs_slab_thickness_mm = find_min_hcs_thickness(s1 / 2, live_load)

        # If still no suitable slab, raise an error
        if hcs_slab_thickness_mm is None:
            raise ValueError("No suitable hollow core slab found for given span and load, even after trying s1/2.")

        slab_thickness_mm = 75
        slab_max_spacing_pt_mm = 0

    return slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm
