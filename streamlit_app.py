import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from io import BytesIO  # For handling the PDF export

# Set the browser tab title and other configurations
st.set_page_config(page_title="DfMA Model", page_icon="📊")

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
    column_size = math.ceil(column_size / 50) * 50

    return column_size

def calculate_beam_size_1way(s1, s2, live_load):
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
    b_to_d_ratio = 1.0  # Beam Width-to-Depth Ratio
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
    d_s1 = ((M_s1) / (0.85 * f_cd * b_to_d_ratio * k_value))**0.5 * correction_factor
    b_s1 = b_to_d_ratio * d_s1  # Width in meters

    # Convert depth and width to mm and round to the nearest 100 mm
    d_s1_mm = round(d_s1 * 1000 / 100) * 100  # Depth in mm
    b_s1_mm = round(b_s1 * 1000 / 100) * 100  # Width in mm

    return b_s1_mm, d_s1_mm


# Function to create a grid plot based on user inputs
def create_grid_plot(length, width, scale):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw boundary
    ax.plot([0, length, length, 0, 0], [0, 0, width, width, 0], color='black', linewidth=2)

    # Draw grid lines
    for x in np.arange(0, length + scale, scale):
        ax.axvline(x, color='gray', linestyle='--', linewidth= 2, alpha=0.7)
    for y in np.arange(0, width + scale, scale):
        ax.axhline(y, color='gray', linestyle='--', linewidth= 0.5, alpha=0.7)
    
     # Set primary axis labels (distances) in between grid lines
    xticks = np.arange(scale / 2, length, scale)  # Midpoints for X-axis
    yticks = np.arange(scale / 2, width, scale)  # Midpoints for Y-axis
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{scale*10}" for _ in xticks])  # Distance labels
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{scale*1000}" for _ in yticks])  # Distance labels
    ax.yaxis.tick_right()


    # Add secondary axis labels (ABCDE and 12345)
    secondary_xticks = np.arange(0, length, scale)  # Original gridline positions
    secondary_yticks = np.arange(0, width, scale)  # Original gridline positions
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
            fontsize=9,
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
            fontsize=9,
            color="black"
        )

    # Remove tick lines
    ax.tick_params(axis="both", which="major", length=0)


    # Set axis limits and labels
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_aspect('equal')
    ax.legend()
    return fig

# Function to save plot to PDF and return as BytesIO
def save_plot_to_pdf(fig):
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    return pdf_bytes

# Streamlit app
st.title("Construction Layout Inputs")

# User inputs for boundaries and grid scale
length = st.number_input("Enter the building length (meters):", min_value=1, value=60)
width = st.number_input("Enter the building width (meters):", min_value=1, value=60)
scale = st.number_input("Enter minimum column spacing (spacing in meters):", min_value=1, value=5)

# Generate and display the grid plot
if st.button("Generate Grid"):
    fig = create_grid_plot(length+2, width+2, scale)
    st.pyplot(fig)

    # Allow user to download the grid plot as a PDF
    pdf_file = save_plot_to_pdf(fig)
    st.download_button(
        label="Download Grid as PDF",
        data=pdf_file,
        file_name=f"grid_{length}x{width}_scale{scale}.pdf",
        mime="application/pdf"
    )
    
# Streamlit app for user interaction
st.title("Size Calculator")

# User inputs
s1 = st.number_input("Enter Beam Span S1 (m):", min_value=0.0, max_value=30.0, step=0.1)
s2 = st.number_input("Enter Beam Span S2 (m):", min_value=0.0, max_value=30.0, step=0.1)
live_load = st.number_input("Enter Live Load (kN/m²):", min_value=0.0, max_value=40.0, step=0.1)


if st.button("Calculate Size"):
    # Calculate column size
    column_size = calculate_column_size(s1, s2, live_load)
    
    # Calculate beam sizes for S1 and S2
    b_s1_mm, d_s1_mm = calculate_beam_size_1way(s1, s2, live_load)
    
    # Display results
    st.write(f"The required column size is: {column_size} mm x {column_size} mm")
    st.write(f"Beam Dimensions: {b_s1_mm} mm x {d_s1_mm} mm")
