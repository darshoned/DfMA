import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO  # For handling the PDF export

# Function to generate the plot
def create_plot(plot_type):
    x = np.linspace(0, 10, 100)
    if plot_type == "Sine":
        y = np.sin(x)
        title = "Sine Wave"
    else:
        y = np.cos(x)
        title = "Cosine Wave"

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    return fig, title

# Function to save plot to PDF and return as BytesIO
def save_plot_to_pdf(fig):
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf')
    pdf_bytes.seek(0)
    return pdf_bytes

# Streamlit app
st.title("Download Sine or Cosine Plot as PDF")

# User input to choose plot type
plot_choice = st.selectbox("Choose the type of plot to generate:", ["Sine", "Cosine"])

# Generate and display the selected plot
fig, plot_title = create_plot(plot_choice)
st.pyplot(fig)

# Allow user to download the plot as a PDF
pdf_file = save_plot_to_pdf(fig)
file_name = f"{plot_title.lower().replace(' ', '_')}_plot.pdf"

st.download_button(
    label=f"Download {plot_choice} Plot as PDF",
    data=pdf_file,
    file_name=file_name,
    mime="application/pdf"
)
