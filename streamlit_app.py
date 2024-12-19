import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO  # For handling the PDF export

# Set the browser tab title and other configurations
st.set_page_config(page_title="DDfMA Grid Plot", page_icon="📊")

# Function to create a grid plot based on user inputs
def create_grid_plot(length, width, scale):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw boundary
    ax.plot([0, length, length, 0, 0], [0, 0, width, width, 0], color='black', linewidth=2)

    # Draw grid lines
    for x in np.arange(0, length + scale, scale):
        ax.axvline(x, color='gray', linestyle='--', alpha=0.7)
    for y in np.arange(0, width + scale, scale):
        ax.axhline(y, color='gray', linestyle='--', alpha=0.7)

    # Set axis limits and labels
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_aspect('equal')
    ax.set_title("Construction Layout")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Width (m)")
    return fig

# Function to save plot to PDF and return as BytesIO
def save_plot_to_pdf(fig):
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    return pdf_bytes

# Streamlit app
st.title("DDfMA Modeling")

# User inputs for boundaries and grid scale
length = st.number_input("Enter the grid length (meters):", min_value=1, value=20)
width = st.number_input("Enter the grid width (meters):", min_value=1, value=15)
scale = st.number_input("Enter the grid scale (spacing in meters):", min_value=1, value=5)

# Generate and display the grid plot
if st.button("Generate Grid"):
    fig = create_grid_plot(length, width, scale)
    st.pyplot(fig)

    # Allow user to download the grid plot as a PDF
    pdf_file = save_plot_to_pdf(fig)
    st.download_button(
        label="Download Grid as PDF",
        data=pdf_file,
        file_name = f"grid_{length}x{width}_scale{scale}.pdf",
        mime="application/pdf"
    )
