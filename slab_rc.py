import math

def calculate_slab_thickness_CIS(s1, s2, live_load,selected_slab):
    """
    Calculate the slab thickness for a one-way reinforced slab based on span and live load.

    Parameters:
    - s1 (float): Span of the slab in meters.
    - live_load (float): Live load in kN/m².

    Returns:
    - float: Recommended slab thickness in meters.
    """

    if selected_slab == "CIS Slab":
    
        # Step 1: Set parameters
        # Span-to-depth ratio adjustments based on loading
        if live_load <= 3:
            span_to_depth_ratio = 25  # Light loading (residential)
        elif 3 < live_load <= 5:
            span_to_depth_ratio = 22  # Medium loading (office/commercial)
        else:
            span_to_depth_ratio = 20  # Heavy loading (industrial)

        # Step 2: Calculate effective depth
        effective_depth = s1 / span_to_depth_ratio  # Effective depth in meters

        # Step 3: Add nominal cover and bar diameter
        nominal_cover = 0.03  # 30 mm nominal cover in meters
        bar_diameter = 0.016  # 16 mm bar diameter in meters
        slab_thickness = effective_depth + nominal_cover + bar_diameter

        # Step 4: Ensure minimum slab thickness
        minimum_thickness = 0.15  # 150 mm minimum thickness in meters
        slab_thickness = max(slab_thickness, minimum_thickness)

        # Step 5: Round up to the nearest 50 mm
        slab_thickness_mm = math.floor(slab_thickness * 1000 / 50) * 50  # Convert to mm and round down
        
        
    if selected_slab == "PT Flat Slab":
    
        # Step 1: Set span-to-depth ratio based on live load
        if live_load <= 3:
            span_to_depth_ratio = 45  # Light loading (residential)
        elif 3 < live_load <= 5:
            span_to_depth_ratio = 40  # Medium loading (office/commercial)
        elif 5 < live_load <= 15:
            span_to_depth_ratio = 35  # Heavy loading (industrial)
        elif 15 < live_load <= 25:
            span_to_depth_ratio = 30  # Heavy loading (industrial)
        else:  # Very heavy loading
            span_to_depth_ratio = 25  # Extreme loading (30 kN/m²)

        # Step 2: Calculate effective depth
        effective_depth = s1 / span_to_depth_ratio  # Effective depth in meters

        # Step 3: Add nominal cover and PT duct space
        nominal_cover = 0.03  # 30 mm nominal cover in meters
        pt_duct_space = 0.02  # 20 mm allowance for PT ducts
        slab_thickness = effective_depth + nominal_cover + pt_duct_space

        # Step 4: Ensure minimum slab thickness
        minimum_thickness = 0.2  # 200 mm minimum thickness for high loads
        slab_thickness = max(slab_thickness, minimum_thickness)

        # Step 5: Round up to the nearest 50 mm
        slab_thickness_mm = math.ceil(slab_thickness * 1000 / 50) * 50  # Convert to mm and round up
     

        # Step 6: Calculate tendon spacing
        # Assume total prestressing force required
        total_prestressing_force = 1.5 * live_load * s1 * s2  # Simplified estimation in kN
        strand_capacity = 300  # kN per strand (15.2 mm strand)

        # Number of tendons required 4 strands in a tendon
        num_tendons = math.ceil(total_prestressing_force / (strand_capacity*4))

        # Calculate maximum tendon spacing
        max_spacing_pt_mm = min(8 * slab_thickness * 1000, s1 * 1000 / num_tendons)  # in mm
        max_spacing_pt_mm = math.floor(max_spacing_pt_mm / 50) * 50  # Round to the nearest 50 mm

        return {
            "slab_thickness_mm": slab_thickness_mm,
            "number_of_tendons": num_tendons,
            "tendon_spacing_mm": max_spacing_pt_mm,
        }

    return slab_thickness_mm, max_spacing_pt_mm
