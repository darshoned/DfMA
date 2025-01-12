import math

def calculate_column_size(s1, s2, live_load,selected_column):
    """
    Calculate the required column size for a 5-storey building with realistic outputs.
    """
    # Material properties and constants
    alpha = 0.85  # Reduction factor for slenderness
    gamma_c = 1.5  # Partial safety factor for concrete
    gamma_s = 1.15  # Partial safety factor for steel
    f_cd = 30 / gamma_c  # Design compressive strength of concrete (C40)
    f_yd = 500 / gamma_s  # Design yield strength of steel (B500)
    reinforcement_ratio = 0.02  # Reinforcement ratio (2%)
    storey_height = 6 #6m f2f

    # Axial resistance
    f_cc = alpha * f_cd
    concrete_contribution = (1 - reinforcement_ratio) * f_cc
    steel_contribution = reinforcement_ratio * f_yd
    axial_resistance = concrete_contribution + steel_contribution  # kN/m²

    # Effective length approximation
    effective_length = storey_height  # Simplified effective length

    # Dead and live load calculations
    dead_load = 27 * s1 * s2 * 5  # Dead load for all 5 storeys (25 kN/m²)
    live_load_total = live_load * s1 * s2 * 5  # Live load for all 5 storeys
    column_self_weight = 0.03 * 25 * effective_length  # Self-weight of column
    total_load = dead_load + live_load_total + column_self_weight  # Total load in kN

    # Required cross-sectional area (mm²)
    required_area = total_load * 1000 / axial_resistance  # Convert kN to N for consistency

    # Calculate column size (square section)
    column_size_mm = math.sqrt(required_area)  # Side length of square column (mm)

    # Enforce minimum practical size and prevent excessive rounding
    column_size_mm = max(column_size_mm, 500)

    # Round up to the nearest 50 mm
    column_size_mm = (math.ceil(column_size_mm / 50) * 50)/1000
    
    if selected_column == "CIS Column":
        # Column weight
        column_weight_tonnes = (column_size_mm/1000) ** 2 * (storey_height) * 2.5 * 0
        
    if selected_column == "PC Column":
        # Column weight
        column_weight_tonnes = (column_size_mm/1000) ** 2 * (storey_height) * 2.5

    return column_size_mm, column_weight_tonnes
