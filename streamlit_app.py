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

# Function to save plot to PDF and return as BytesIO
#def save_plot_to_pdf(fig):
#    pdf_bytes = BytesIO()
#    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
#    pdf_bytes.seek(0)
#    return pdf_bytes

# Streamlit app
st.title("DfMA Model Inputs")

# Define the options for columns, beams, and slabs
column_options = [
    "CIS Column",
    "PC Column",
    "Steel Column (Not Available)",
    "CES Column (Not Available)",
    "SEC Column (Not Available)",
]

beam_options = [
    "CIS Beam",
    "PT Beam",
    "PT Flat Slab",
    "CES Beam (Not Available)",
    "I Beam (Not Available)",
    "Castellated I Beam (Not Available)",
]

slab_options = [
    "CIS Slab",
    "1.2HC Slab",
    "2.4HC Slab",
    "PT Flat Slab",
    "Bubble Deck Slab (Not Available)",
    "DoubleTee Slab (Not Available)",
    "Bondek (Not Available)",
]

# Step 1: Create the dropdown menus
selected_column = st.selectbox("Select Column Type:", options=column_options)
selected_beam = st.selectbox("Select Beam Type:", options=beam_options)
selected_slab = st.selectbox("Select Slab Type:", options=slab_options)

# Step 2: Define multiple available combinations
available_combinations = [
    {"beam": "CIS Beam", "slab": "CIS Slab", "column": "CIS Column"},
    {"beam": "CIS Beam", "slab": "CIS Slab", "column": "PC Column"},
    {"beam": "CIS Beam", "slab": "1.2HC Slab", "column": "CIS Column"},
    {"beam": "CIS Beam", "slab": "1.2HC Slab", "column": "PC Column"},
    {"beam": "CIS Beam", "slab": "2.4HC Slab", "column": "CIS Column"},
    {"beam": "CIS Beam", "slab": "2.4HC Slab", "column": "PC Column"},
    {"beam": "PT Beam", "slab": "CIS Slab", "column": "CIS Column"},
    {"beam": "PT Beam", "slab": "CIS Slab", "column": "PC Column"},
    {"beam": "PT Beam", "slab": "1.2HC Slab", "column": "CIS Column"},
    {"beam": "PT Beam", "slab": "1.2HC Slab", "column": "PC Column"},
    {"beam": "PT Beam", "slab": "2.4HC Slab", "column": "CIS Column"},
    {"beam": "PT Beam", "slab": "2.4HC Slab", "column": "PC Column"},
    {"beam": "PT Flat Slab", "slab": "PT Flat Slab", "column": "CIS Column"},
    {"beam": "PT Flat Slab", "slab": "PT Flat Slab", "column": "PC Column"},
]

# Step 3: Check if the selected combination matches any available option
selected_combination = {
    "beam": selected_beam,
    "slab": selected_slab,
    "column": selected_column,
}

if selected_combination in available_combinations:
    st.success("You selected a valid combination!")
else:
    st.warning("The selected combination is not available. Please choose a valid option.")

s1 = st.number_input("Enter Beam Span S1 (Required Column to Column clear distance) (m):", min_value=5, max_value=13, step=1, value=10)
s2 = st.number_input("Enter Beam Span S2 (may be adjusted based on chosen structure design) (m):", min_value=0, max_value=12, step=1, value=10)
live_load = st.number_input("Enter Live Load (kN/m²):", min_value=0.0, max_value=20.0, step=0.1, value=3.0)
lengthinput = st.number_input("Enter the building length (meters):", min_value=20, max_value=100, step=1, value=60)
widthinput = st.number_input("Enter the building width (meters):", min_value=20, max_value=40, step=1, value=40)
f2f = st.number_input("Enter the F2F Height (meters):", min_value=2, max_value=6, step=1, value=6)
length = math.floor((lengthinput) / s1) * s1
width = math.floor((widthinput) / s2) * s2

# Generate and display the gri d plot
if st.button("Generate"):
    from column_rc import calculate_column_size
    from beam_rc import calculate_beam_size
    from slab_rc import calculate_slab_thickness
    from slab_rc import hcs_selected_slab_check
    from output_data import calculate_layout_outputs
    from plot_data import create_grid_plot
    
    column_size_mm, column_weight_tonnes = calculate_column_size(s1, s2, live_load,selected_column, f2f)
    selected_slab = hcs_selected_slab_check(s1, live_load, selected_slab)
    b_s1_mm, d_s1_mm, b_s2_mm, d_s2_mm, b_s3_mm, d_s3_mm = calculate_beam_size(s1, s2, live_load, column_size_mm, selected_beam, selected_slab)
    slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm = calculate_slab_thickness(s1, s2, live_load,selected_slab)
    misc_output, design_output, equipment_output, utility_output, manpower_output, beam_manhour, column_manhours, slab_manhours, casting_manhours = calculate_layout_outputs(s1, s2, live_load, column_size_mm, selected_column, selected_beam, selected_slab, length, width, b_s1_mm, d_s1_mm,b_s2_mm, d_s2_mm, b_s3_mm, d_s3_mm, slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm, f2f) 
    fig = create_grid_plot(length, width, s1, s2, live_load,selected_column, selected_beam, selected_slab, column_size_mm, column_weight_tonnes, b_s1_mm, d_s1_mm, b_s2_mm, d_s2_mm, b_s3_mm, d_s3_mm, slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm)
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
            "Weight of loose rebar (tonnes)",
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
            "Expected Mandays (Structure only)",
            "Floor cycle(days)",
            "Unique Headcount"
        ],
        "Value": manpower_output
    }
    
    miscellaneous_data = {
    "Category": [
        "Number of volumetric precast component(s)",
        "Number of vertical precast component(s)",
        "Number of propped horizontal component(s)",
        "Number of unpropped horizontal component(s)",
        "Formwork area for slab(s)",
        "Formwork area for beam(s)",
        "Number of column formwork(s)",
        "Weight of loose rebar (tonnes)",
        "Weight of slab rebar (tonnes)",
        "CIS Volume(m3)",
        "Number of tower crane(s)",
        "Number of concrete pump(s)",
        "Number of passenger/material hoist(s)",
        "Number of construction hoist(s)",
        "Number of Gondola(s)",
        "Number of MEWP(s)",
        "Hoist Count passenger/material hoist",
        "Hoist Count Tower Crane",
        "Number of concrete truck delivery(s)",
        "Number of trailer delivery(s)",
        "Beam manhours",
        "Slab manhours",
        "Column manhours",
        "Casting manhours",
        "Total Mandays (Structure only)",
        "Total Productivity m2/manday (Structure only)",
        "Slab CIS Volume (m³)",
        "Beam CIS Volume (m³)",
        "Column CIS Volume (m³)",
        "Weight of beam rebar (tonnes)",
        "Weight of column rebar (tonnes)",
        "Weight of slab rebar (tonnes)",
        "Weight of loose rebar (tonnes)",
        "Beam Hoist Count (Tower Crane)",
        "Slab Hoist Count (Tower Crane)",
        "Column Hoist Count (Tower Crane)"
    ],
        "Value": misc_output
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
    #df_misc = pd.DataFrame(miscellaneous_data)

    # Streamlit Layout
    st.title("Data Tables")

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
        
    # Streamlit Layout
    #st.title("Additional Miscellaneous Data")

    # Display miscellaneous outputs
    #st.subheader("Miscellaneous Outputs")
    #st.markdown(create_html_table(df_misc), unsafe_allow_html=True)







