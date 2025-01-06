import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as transforms
import numpy as np
import math
import shapely
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import Polygon
from io import BytesIO  # For handling the PDF export

# Set the browser tab title and other configurations
st.set_page_config(page_title="DfMA Model", page_icon="📊")

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
        if length <= 40:
            no_tower_cranes = 1
        elif 40 < length <= 70:
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
        round(total_productivity_crane,2),
        round(total_productivity_crane/2,2)
        ]

    return design_output,equipment_output,utility_output,manpower_output, beam_manhours, column_manhours, slab_manhours, casting_manhours


def calculate_slab_thickness_CIS(s1, live_load):
    """
    Calculate the slab thickness for a one-way reinforced slab based on span and live load.

    Parameters:
    - s1 (float): Span of the slab in meters.
    - live_load (float): Live load in kN/m².

    Returns:
    - float: Recommended slab thickness in meters.
    """

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
    slab_thickness = slab_thickness_mm / 1000  # Convert back to meters

    return slab_thickness

def calculate_column_size(s1, s2, live_load):
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

    # Axial resistance
    f_cc = alpha * f_cd
    concrete_contribution = (1 - reinforcement_ratio) * f_cc
    steel_contribution = reinforcement_ratio * f_yd
    axial_resistance = concrete_contribution + steel_contribution  # kN/m²

    # Effective length approximation
    effective_length = max(s1, s2) / 2  # Simplified effective length

    # Dead and live load calculations
    dead_load = 27 * s1 * s2 * 5  # Dead load for all 5 storeys (25 kN/m²)
    live_load_total = live_load * s1 * s2 * 5  # Live load for all 5 storeys
    column_self_weight = 0.03 * 25 * effective_length  # Self-weight of column
    total_load = dead_load + live_load_total + column_self_weight  # Total load in kN

    # Required cross-sectional area (mm²)
    required_area = total_load * 1000 / axial_resistance  # Convert kN to N for consistency

    # Calculate column size (square section)
    column_size = math.sqrt(required_area)  # Side length of square column (mm)

    # Enforce minimum practical size and prevent excessive rounding
    column_size = max(column_size, 500)

    # Round up to the nearest 50 mm
    column_size = (math.ceil(column_size / 50) * 50)/1000

    return column_size

def calculate_beam_size_1way(s1, s2, live_load, column_size):
    """
    Calculate the required beam size for a 1-way slab with S1 as the loaded beam.
    :param s1: Span of the beam in meters.
    :param s2: Tributary width for the beam in meters.
    :param live_load: Live load in kN/m².
    :return: Required beam width and depth in mm, rounded to the nearest 100 mm.
    """

    # Material properties and constants
    gamma_c = 1.0  # Partial safety factor for concrete
    f_cd = 40 / gamma_c  # Design compressive strength of concrete (C40) in MPa
    dead_load = 7.0  # Dead load in kN/m²
    b_to_d_ratio = 0.8  # Beam Width-to-Depth Ratio
    reinforcement_ratio = 0.04  # Reinforcement ratio
    f_y = 500  # Yield strength of steel in MPa
    k_value = 0.167  # Assumed constant from design tables

    # Total load per unit area
    q_total = dead_load + live_load  # kN/m²

    # Load per unit length of the beam
    w_s1 = q_total * s2  # Load on the beam in S1 direction (kN/m)

    # Maximum bending moment (for a continuous beam with uniformly distributed load)
    M_s1 = (w_s1 * s1**2) / 16  # Bending moment in kNm

    # Refined heuristic-based correction factor from ML insights
    def ml_correction_factor(s1, s2, live_load):
        # Updated coefficients from Random Forest model
        intercept = 0.6224334123549233
        coef_s1 = -0.31497491902711683
        coef_s2 = -0.2956838878494714
        coef_ll = -0.38934119312341176

        # Compute correction factor
        correction_factor = intercept + (coef_s1 * s1) + (coef_s2 * s2) + (coef_ll * live_load)
        return max(0.1, min(1.0, correction_factor))

    correction_factor = ml_correction_factor(s1, s2, live_load)

    # Adjusted calculation with heuristic-based correction factor
    d_s2 = ((M_s1) / (0.85 * f_cd * b_to_d_ratio * k_value))**0.5 * correction_factor
    b_s2 = b_to_d_ratio * d_s2  # Width in meters

    # Convert depth and width to mm and round to the nearest 100 mm
    d_s2_mm = round(d_s2 * 1000 / 100) * 100  # Depth in mm
    b_s2_mm = round(b_s2 * 1000 / 100) * 100  # Width in mm
    b_s2_mm = min(b_s2_mm, column_size*1000)
    b_s2_mm = round(b_s2_mm, 0)

    return b_s2_mm, d_s2_mm

def calculate_unloaded_beam(s1, column_size):
    b_s1_mm = column_size * 1000
    d_s1 = s1 /15
    d_s1_mm = round(d_s1 * 1000 / 100) * 100  # Depth in mm
    d_s1_mm = min(d_s1_mm,b_s1_mm)
    return b_s1_mm, d_s1_mm

# Function to create a grid plot based on user inputs
def create_grid_plot(length, width, s1, column_size, s2, structure_type, b_s2_mm, d_s2_mm, b_s1_mm, d_s1_mm, slab_thickness):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw boundary
    ax.plot([0, (length + 2* s1), (length + 2* s1), 0, 0], [0, 0, (width + 2 * s2), (width + 2 * s2), 0], color='black', linewidth=2)

    # Draw grid lines
    for x in np.arange(0, length + 2 * s1, s1):
        ax.axvline(x, color='gray', linestyle='--', linewidth= 0.3, alpha=0.7)
    for y in np.arange(0, width + 2 * s2, s2):
        ax.axhline(y, color='gray', linestyle='--', linewidth= 0.3, alpha=0.7)
    
     # Set primary axis labels (distances) in between grid lines
    xticks = np.arange(s1 / 2, length + 2 * s1, s1)  # Midpoints for X-axis
    yticks = np.arange(s2 / 2, width + 2 * s2, s2)  # Midpoints for Y-axis
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{s1*1000}" for _ in xticks], rotation=90, fontsize=8)  # Distance labels
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{s2*1000}" for _ in yticks], fontsize=8)  # Distance labels
    ax.yaxis.tick_right()


    # Add secondary axis labels (ABCDE and 12345)
    secondary_xticks = np.arange(0, length + 2 * s1, s1)  # Original gridline positions
    secondary_yticks = np.arange(0, width + 2 * s2, s2)  # Original gridline positions
    secondary_horizontal_labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:len(secondary_xticks)]
    secondary_vertical_labels = list(range(1, len(secondary_yticks) + 1))

    # Add secondary labels above the X-axis
    for i, label in enumerate(secondary_horizontal_labels):
        ax.text(
            secondary_xticks[i],
            ax.get_ylim()[1],  # Offset above the axis
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="black"
        )

    # Add secondary labels to the left of the Y-axis
    for i, label in enumerate(secondary_vertical_labels):
        ax.text(
            ax.get_xlim()[0] - 1,  # Offset to the left of the axis
            secondary_yticks[i],
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="black"
        )

    # Remove tick lines
    ax.tick_params(axis="both", which="major", length=0)


    # Set axis limits and labels
    ax.set_xlim(0, length + 2 * s1)
    ax.set_ylim(0, width + 2 * s2)
    ax.set_aspect('equal')
    

    # Plot Columns
    for x in np.arange(s1, length + 2 * s1, s1):
        for y in np.arange(s2, width + 2 * s2, s2):
            ax.fill([
                x - column_size/2, x + column_size/2, x + column_size/2, x - column_size/2, x - column_size/2
            ], [
                y - column_size/2, y - column_size/2, y + column_size/2, y + column_size/2, y - column_size/2
            ], color='black', linewidth=0.3)
            
    # Plot s1
    for x in np.arange(s1, length+s1, s1):
        for y in np.arange(s2, width + 2*s2, s2):        
            
            ax.plot([
                x + column_size/2, x + column_size/2, x + s1 - column_size/2, x + s1 - column_size/2, x + column_size/2
            ], [
                y - column_size/2, y + column_size/2, y + column_size/2, y - column_size/2, y - column_size/2
            ], color='black', linewidth=0.3, linestyle='--')
            
    # Plot s2
    for x in np.arange(s1, length + 2*s1, s1):
        for y in np.arange(s2, width+s2, s2):        
            
            ax.plot([
                x - column_size/2, x - column_size/2, x + column_size/2, x + column_size/2, x - column_size/2
            ], [
                y + column_size/2, y + column_size/2 + s2, y + column_size/2 + s2, y + column_size/2, y + column_size/2
            ], color='black', linewidth=0.3, linestyle=':')
            
            
    # Call secondary element plot function
    plot_staircase(ax, s1, s2, column_size, length, width)
    plot_crane(ax, width, length)
    
    # Plot Slab
    if structure_type == "CIS Beam + CIS Slab + CIS Column":
        for x in np.arange(s1, length + 2* s1, s1):
            for y in np.arange(s2, width + 2* s2, s2):        
                ax.text(x + s1/2, y + s2/2, '~', fontsize=8, color='black', ha='center', va='center')
                
    if structure_type == "CIS Beam + CIS Slab + CIS Column":
        ax.text(length + (0.5*s1), 0.5* s2, f"{b_s1_mm:.0f} × \n {d_s1_mm}(d) mm" ,  # Text content
                fontsize=4,
                color='black',
                ha='center',  # Horizontal alignment
                va='center',  # Vertical alignment
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
        
        ax.text(length + (1.5*s1), 1.5* s2, f"{b_s2_mm:.0f} × \n {d_s2_mm}(d) mm" ,  # Text content
                fontsize=4,
                color='black',
                ha='center',  # Horizontal alignment
                va='center',  # Vertical alignment
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))    
        
    # Create a filled square for the legend
    column_legend = mpatches.Patch(color='black', label=f"Column {column_size*1000:.0f} x {column_size*1000:.0f}mm ")

    slab_legend = mpatches.Rectangle(
    (0, 0),  # Dummy position
    width=1,  # Width in data units (not used in legend)
    height=0.5,  # Height in data units (not used in legend)
    edgecolor="black",
    facecolor="none",
    label=f"~ One Way Slab{slab_thickness*1000:.0f} mm"
    )
    
    # Add legend with the filled square
    ax.legend(handles=[column_legend, slab_legend], loc='upper left',
    bbox_to_anchor=(0.0, -0.2),  # Place the legend below the plot
    ncol=1,  # Arrange the legend entries in 2 columns
    fontsize=4)
    
    
    
    return fig

def plot_staircase(ax, s1, s2, column_size, length, width):
    """
    Plot a staircase layout within the grid (plan view).
    """
    # Staircase parameters (in meters)
    floor_to_floor_height = 6.0  # m
    riser_height = 0.15  # m
    tread_depth = 0.3  # m
    landing_length = 2  # m
    stair_width = 1.2  # m
    wall_width = 0.2
    Lift_external = 2.5

    # Calculate number of risers and treads
    num_risers = int(floor_to_floor_height / riser_height)
    num_treads_per_flight = (num_risers // 2) - 1

    # First flight of stairs 1
    for i in range(num_treads_per_flight):
        x_start = i * tread_depth + s1 + landing_length + column_size/2
        x_end = x_start + tread_depth
        y_start = s2 - column_size/2 - stair_width - wall_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Second flight of stairs 1
    for i in range(num_treads_per_flight):
        x_start = i * tread_depth + s1 + landing_length + column_size/2
        x_end = x_start + tread_depth
        y_start = s2 - column_size/2 - stair_width - stair_width - wall_width - wall_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Intermediate landing 1
    landing_start = s1 + column_size/2
    landing_end = landing_start + landing_length
    y_start = s2 - column_size/2 - stair_width - stair_width - wall_width - wall_width
    y_end = s2 - column_size/2
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)

    # 2nd Intermediate landing 1
    landing_start = s1 + column_size/2 + num_treads_per_flight*tread_depth + landing_length
    landing_end = landing_start + landing_length
    y_start = s2 - column_size/2 - stair_width - stair_width - wall_width - wall_width
    y_end = y_start + stair_width + stair_width + wall_width
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)
    
    # Wall1
    wall_end = s1 + column_size/2 + num_treads_per_flight*tread_depth + 2 * landing_length
    wall_start = s1 + column_size/2
    wall_intermediate = s1 + column_size/2 + landing_length
    ywall_start = s2 - column_size/2 - stair_width - stair_width - wall_width - wall_width
    ywall_end = y_start + stair_width + stair_width + wall_width
    ax.plot([wall_start - wall_width, wall_start - wall_width, wall_end + wall_width, wall_end + wall_width, wall_intermediate], [ywall_end, ywall_start - wall_width, ywall_start - wall_width, ywall_end + wall_width, ywall_end + wall_width], color='black', linewidth=0.1)

    # lift1
    corner_x = s1 - column_size/2
    corner_large = s2 + column_size/2
    corner_small = s2 + column_size/2 + wall_width
    ax.plot([corner_x, corner_x-Lift_external, corner_x-Lift_external, corner_x], [corner_large, corner_large, corner_large+Lift_external, corner_large+Lift_external], color='black', linewidth=0.1)
    ax.plot([corner_x, corner_x-Lift_external+wall_width, corner_x-Lift_external+wall_width, corner_x], [corner_small, corner_small, corner_small+Lift_external-wall_width-wall_width, corner_small+Lift_external-wall_width-wall_width], color='black', linewidth=0.1)

    # First flight of stairs 2
    for i in range(num_treads_per_flight):
        x_start = length + s1 - (i * tread_depth) - landing_length
        x_end = x_start - tread_depth
        y_start = width + s2 + column_size/2 + wall_width
        y_end = y_start + stair_width 
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Second flight of stairs 2
    for i in range(num_treads_per_flight):
        x_start = length + s1 - (i * tread_depth) - landing_length 
        x_end = x_start - tread_depth
        y_start = width + s2 + column_size/2 + wall_width + wall_width + stair_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)
        
    # Intermediate landing 2
    landing_start = length + s1 - landing_length - column_size/2 + tread_depth
    landing_end = landing_start + landing_length
    y_start = width + s2 + column_size/2 + wall_width + wall_width + stair_width + stair_width
    y_end = width + s2 + column_size/2 + wall_width
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)

    # 2nd Intermediate landing 2
    landing_start = length + s1 - landing_length - column_size/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length
    landing_end = landing_start + landing_length
    y_start = width + s2 + column_size/2 + wall_width + wall_width + stair_width + stair_width
    y_end = width + s2 + column_size/2
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)
    
     # Wall1
    wall_end = length + s1 - landing_length - column_size/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length + num_treads_per_flight*tread_depth + 2 * landing_length
    wall_start = length + s1 - landing_length - column_size/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length
    wall_intermediate = length + s1 - landing_length - column_size/2 + tread_depth - num_treads_per_flight*tread_depth
    ywall_start = width + s2 + column_size/2
    ywall_end = ywall_start + (2 * stair_width) + (3 * wall_width)
    ax.plot([wall_start - wall_width, wall_start - wall_width, wall_end + wall_width, wall_end + wall_width, wall_intermediate], [ywall_start, ywall_end, ywall_end, ywall_start, ywall_start], color='black', linewidth=0.1)

    # lift2
    corner_x = length + s1 + column_size/2
    corner_large = width + s2 - column_size/2
    corner_small = width + s2 - column_size/2 + wall_width
    ax.plot([corner_x, corner_x+Lift_external, corner_x+Lift_external, corner_x], [corner_large, corner_large, corner_large-Lift_external, corner_large-Lift_external], color='black', linewidth=0.1)
    ax.plot([corner_x, corner_x+Lift_external+wall_width, corner_x+Lift_external+wall_width, corner_x], [corner_small, corner_small, corner_small-Lift_external-wall_width-wall_width, corner_small-Lift_external-wall_width-wall_width], color='black', linewidth=0.1)

def plot_crane(ax, width, length):
    # Determine number of cranes based on length
    if length <= 30:
        centers = [((length+2*s1) / 2, (width+2*s2) / 2)]
    elif 30 < length <= 60:
        centers = [((length+2*s1) / 3, (width+2*s2) / 2), (2 * (length+2*s1) / 3, (width+2*s2) / 2)]
    elif 60 < length <= 100:
        centers = [((length+2*s1) / 4, (width+2*s2) / 2), ((length+2*s1) / 2, (width+2*s2) / 2), (3 * (length+2*s1) / 4, (width+2*s2) / 2)]

    # Plot each crane
    for center_x, center_y in centers:
        # Define squares (relative to the crane center)
        square_2_3 = np.array([[-1.15, -1.15], [1.15, -1.15], [1.15, 1.15], [-1.15, 1.15], [-1.15, -1.15]]) + [center_x, center_y]
        square_5 = np.array([[-2.5, -2.5], [2.5, -2.5], [2.5, 2.5], [-2.5, 2.5], [-2.5, -2.5]]) + [center_x, center_y]

        # Plot squares
        ax.plot(square_2_3[:, 0], square_2_3[:, 1], color="blue", linewidth=1, label="2.3m Square" if center_x == centers[0][0] else None)
        ax.plot(square_5[:, 0], square_5[:, 1], color="green", linewidth=1, label="5m Square" if center_x == centers[0][0] else None)

        # Draw a cross in the 2.3m square
        ax.plot([center_x - 1.15, center_x + 1.15], [center_y, center_y], color="red", linewidth=1)  # Horizontal line
        ax.plot([center_x, center_x], [center_y - 1.15, center_y + 1.15], color="red", linewidth=1)  # Vertical line

        # Draw two circles (15m and 30m radius) centered at the crane
        circle_15 = plt.Circle((center_x, center_y), 15, color="purple", fill=False, linewidth=1, label="15m Circle" if center_x == centers[0][0] else None)
        circle_30 = plt.Circle((center_x, center_y), 30, color="orange", fill=False, linewidth=1, label="30m Circle" if center_x == centers[0][0] else None)
        ax.add_patch(circle_15)
        ax.add_patch(circle_30)

# Function to save plot to PDF and return as BytesIO
def save_plot_to_pdf(fig):
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    return pdf_bytes

# Streamlit app
st.title("DfMA Model Inputs")

# User inputs for boundaries and grid scale

s1 = st.number_input("Enter Beam Span S1 (Required Column to Column clear distance) (m):", min_value=5, max_value=20, step=1, value=8)
s2 = st.number_input("Enter Beam Span S2 (may be adjusted based on chosen structure design) (m):", min_value=0, max_value=20, step=1, value=4)
live_load = st.number_input("Enter Live Load (kN/m²):", min_value=0.0, max_value=8.0, step=0.1, value=3.0)
lengthinput = st.number_input("Enter the building length (meters):", min_value=20, max_value=100, step=1, value=60)
widthinput = st.number_input("Enter the building width (meters):", min_value=20, max_value=40, step=1, value=30)
length = math.ceil((lengthinput) / s1) * s1
width = math.ceil((widthinput) / s2) * s2

options = [
    "CIS Beam + CIS Slab + CIS Column",
    "CIS Beam + CIS Slab + PC Column",
    "CIS Beam + 1.2HC Slab + CIS Column",
    "CIS Beam + 1.2HC Slab + PC Column",
    "PT Beam + 1.2HC Slab + CIS Column",
    "PT Beam + 1.2HC Slab + PC Column",
    "PT Flat Slab and Beam + CIS Column",
    "PT Flat Slab and Beam + PC Column",
    "PT Beam + DoubleTee Slab + CIS Column",
    "PT Beam + DoubleTee Slab + PC Column",
    "I Beam + Bondek + CIS Column",
    "I Beam + Bondek + PC Column",
    "I Beam + Bondek + CES Column",
    "I Beam + Bondek + SEC Column",
    ]

    # Step 2: Create the selectbox
structure_type = st.selectbox("Select Structure Type:", options=options)

    # Step 3: Check the selected option
if structure_type == "CIS Beam + CIS Slab + CIS Column":
    st.success("You selected the available option!")
else:
    st.warning("The selected structure type is currently not available. Please select 'CIS Beam + CIS Slab + CIS Column'.")

# Generate and display the grid plot
if st.button("Generate Grid"):
    column_size = calculate_column_size(s1, s2, live_load)
    b_s2_mm, d_s2_mm = calculate_beam_size_1way(s1, s2, live_load, column_size)
    b_s1_mm, d_s1_mm = calculate_unloaded_beam(s1, column_size)
    slab_thickness = calculate_slab_thickness_CIS(s1, live_load)
    design_output, equipment_output, utility_output, manpower_output, beam_manhour, column_manhours, slab_manhours, casting_manhours = Calculate_Layout_outputs(s1, s2, live_load, column_size, structure_type, length, width,b_s1_mm, d_s1_mm,b_s2_mm, d_s2_mm, slab_thickness)
    fig = create_grid_plot(length, width, s1, column_size, s2, structure_type, b_s2_mm, d_s2_mm,b_s1_mm, d_s1_mm, slab_thickness)
    st.pyplot(fig)
    #st.write(beam_manhour)
    #st.write(column_manhours)
    #st.write(slab_manhours)
    #st.write(casting_manhours)
    
   # # Allow user to download the grid plot as a PDF
    #pdf_file = save_plot_to_pdf(fig)
    #st.download_button(
    #    label="Download Grid as PDF",
    #    data=pdf_file,
    #    file_name=f"grid_{length}x{width}_scale.pdf",
    #    mime="application/pdf")

    st.markdown(
        """
        <style>
        .streamlit-table td {
            word-wrap: break-word;
            word-break: break-word;
            white-space: normal;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Design Data
    design_data = {
        "Category": [
            "Number of volumetric precast component(s)",
            "Number of vertical precast component(s)",
            "Number of propped horizontal component(s)",
            "Number of unpropped horizontal component(s)",
            "Formwork area for slab(s)",
            "Formwork area for beam(s)",
            "Number of column formwork(s)",
            "Weight of beam rebar (tonnes)",
            "Weight of slab rebar (tonnes)",
            "CIS Volume(m3)"
        ],
        "Value": design_output
    }

    # Equipment Data
    equipment_data = {
        "Category": [
            "Number of tower crane(s)",
            "Number of concrete pump(s)",
            "Number of passenger/material hoist(s)",
            "Number of construction hoist(s)",
            "Number of Gondola(s)",
            "Number of MEWP(s)"
        ],
        "Value": equipment_output
    }

    # Equipment Utility
    utility_data = {
        "Category": [
            "Hoist Count passenger/material hoist",
            "Hoist Count Tower Crane",
            "Number of concrete truck delivery(s)",
            "Number of trailer delivery(s)"
        ],
        "Value": utility_output
    }

    # Manpower Data
    manpower_data = {
        "Category": [
            "Total Mandays (Structure only)",
            "Total Productivity m2/manday(Structure only)",
            "Total Productivity m2/manday(Total)",
        ],
        "Value": manpower_output
    }


    # Convert data to HTML tables
    def create_html_table(data):
        html = "<table class='custom-table'>"
        html += "<thead><tr><th>Category</th><th>Value</th></tr></thead><tbody>"
        for _, row in data.iterrows():
            html += f"<tr><td>{row['Category']}</td><td>{row['Value']}</td></tr>"
        html += "</tbody></table>"
        return html

    # Create DataFrames
    df_design = pd.DataFrame(design_data)
    df_equipment = pd.DataFrame(equipment_data)
    df_utility = pd.DataFrame(utility_data)
    df_manpower = pd.DataFrame(manpower_data)

    # Streamlit Layout
    st.title("Construction Data Tables")

        # First Row: Design and Equipment
    col1, col2 = st.columns(2)  # Two columns in the first row

    with col1:
        st.subheader("Design")
        st.markdown(create_html_table(df_design), unsafe_allow_html=True)

    with col2:
        st.subheader("Equipment")
        st.markdown(create_html_table(df_equipment), unsafe_allow_html=True)

    # Second Row: Utility and Manpower
    col3, col4 = st.columns(2)  # Two columns in the second row

    with col3:
        st.subheader("Utility")
        st.markdown(create_html_table(df_utility), unsafe_allow_html=True)

    with col4:
        st.subheader("Manpower")
        st.markdown(create_html_table(df_manpower), unsafe_allow_html=True)

# Generate plot data based on live loads
#if st.button("Plot Live Load vs Total Productivity"):
    
   # live_loads = np.arange(1, 6, 1)  # Live load values from 1 to 5 (kN/m²)
   # productivity_values = []
   # for live_load in live_loads:
        # Recalculate outputs for each live load
   #     s1= 8
    #    s2=4
     #   length = 60
      #  width = 30
       # column_size = calculate_column_size(s1, s2, live_load)
        #b_s2_mm, d_s2_mm = calculate_beam_size_1way(s1, s2, live_load, column_size)
        #b_s1_mm, d_s1_mm = calculate_unloaded_beam(s1, column_size)
        #slab_thickness = calculate_slab_thickness_CIS(s1, live_load)
        #design_output, equipment_output, utility_output, manpower_output, beam_manhour, column_manhours, slab_manhours, casting_manhours = Calculate_Layout_outputs(
        #    s1, s2, live_load, column_size, structure_type, length, width, b_s1_mm, d_s1_mm, b_s2_mm, d_s2_mm, slab_thickness
        #)
        #
        # Extract total productivity from manpower_output (third array element)
        #total_productivity = manpower_output[2]  # Assuming third element is total productivity
        #productivity_values.append(total_productivity)

    # Plotting
    #fig, ax = plt.subplots()
    #ax.plot(live_loads, productivity_values, marker='o', linestyle='-', color='blue')
    #ax.set_title("Live Load vs Total Productivity", fontsize=16)
    #ax.set_xlabel("Live Load (kN/m²)", fontsize=12)
    #ax.set_ylabel("Total Productivity (m²/manday)", fontsize=12)
    #ax.grid(True)
    #st.pyplot(fig)
