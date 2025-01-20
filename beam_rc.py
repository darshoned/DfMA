import math

def calculate_beam_size(s1, s2, live_load, column_size_mm, selected_beam, dead_load=7.0, f_ck=40, b_to_d_ratio=0.5, k_con=0.167, k_pt = 0.25,
    gamma_c=1.5, gamma_s=1.15, gamma_DL=1.35, gamma_LL=1.5):
    """
    Calculate beam depth and width for given parameters with safety factors applied.
    
    Args:
    - s1 (float): Beam span in meters.
    - s2 (float): Slab width (load contribution) in meters.
    - live_load (float): Live load in kN/m².
    - dead_load (float): Dead load in kN/m² (default = 7.0).
    - f_ck (float): Characteristic compressive strength of concrete in MPa (default = 30 MPa).
    - b_to_d_ratio (float): Width-to-depth ratio for beam (default = 0.5).
    - k (float): Coefficient for bending moment calculation (default = 0.167).
    - gamma_c (float): Partial safety factor for concrete (default = 1.5).
    - gamma_s (float): Partial safety factor for steel (default = 1.15).
    - gamma_DL (float): Partial safety factor for dead load (default = 1.35).
    - gamma_LL (float): Partial safety factor for live load (default = 1.5).

    Returns:
    - s1_depth_mm (float): Required beam depth in mm.
    - s1_width_mm (float): Corresponding beam width in mm.
    """
    # Apply safety factors to loads

    design_dead_load = dead_load * gamma_DL
    design_live_load = live_load * gamma_LL
    q_total = design_dead_load + design_live_load  # kN/m²

    # Apply safety factor to concrete
    f_cd = f_ck / gamma_c  # Design compressive strength of concrete in MPa

    # Load per unit length of beam
    w = q_total * s2  # kN/m

    # Maximum bending moment (simply supported beam)
    M = (w * s1**2) / 8  # Bending moment in kNm
    M_Nmm = M * 1e6  # Convert kNm to Nmm
    
    if selected_beam == "CIS Beam":

     # Calculate required depth (d)
        b_s2_mm = 300  # Default initial beam width in mm
        d_s2_mm = math.sqrt(M_Nmm / (k_con * b_s2_mm * f_cd))  # Depth in mm

        # Adjust width to maintain width-to-depth ratio
        b_s2_mm = d_s2_mm * b_to_d_ratio  # Corresponding width in mm
        b_s2_mm = max(column_size_mm*1000,b_s2_mm)
        d_s2_mm = round(d_s2_mm / 100) * 100 
    
        b_s1_mm = column_size_mm * 1000
        d_s1 = s1 /15 #1:15 conventional
        d_s1_mm = round(d_s1 * 1000 / 100) * 100  # Depth in mm
        d_s1_mm = max(d_s1_mm,b_s1_mm)
        
    if selected_beam == "PT Beam":

     # Calculate required depth (d)
        b_s2_mm = 300  # Default initial beam width in mm
        d_s2_mm = math.sqrt(M_Nmm / (k_pt * b_s2_mm * f_cd))  # Depth in mm

        # Adjust width to maintain width-to-depth ratio
        b_s2_mm = d_s2_mm * b_to_d_ratio  # Corresponding width in mm
        d_s2_mm = round(d_s2_mm / 100) * 100 
        b_s2_mm = round(b_s2_mm / 100) * 100
    
        b_s1_mm = column_size_mm * 1000
        d_s1 = s1 /15 #1:20 pt
        d_s1_mm = round(d_s1 * 1000 / 100) * 100  # Depth in mm
        d_s1_mm = min(d_s1_mm,b_s1_mm)
        
    if selected_beam == "PT Flat Slab":

        b_s2_mm = 0
        d_s2_mm = 0
        b_s1_mm = 0
        d_s1_mm = 0
    
    return int(b_s1_mm), int(d_s1_mm), int(b_s2_mm), int(d_s2_mm)
