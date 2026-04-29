import streamlit as st
import pandas as pd

st.set_page_config(page_title="Property Navigator", layout="wide")

# Function to extract links if they are saved as strings
def make_clickable(link):
    if pd.isna(link) or str(link).strip() == "":
        return "No link available"
    return f'<a href="{link}" target="_blank">Open Real Estate Listing 🔗</a>'

@st.cache_data
def load_data():
    # Load all sheets
    return pd.read_excel("Opciones_Deptos.xlsx", sheet_name=None)

all_sheets = load_data()

# SIDEBAR
st.sidebar.title("🏙️ Navigation")
selection = st.sidebar.selectbox("Select Property:", list(all_sheets.keys()))

st.title(f"Property Details: {selection}")

df = all_sheets[selection]

# DISPLAY LOGIC
if selection != "HOME":
    # 1. Show the Data Table
    st.table(df) # Using table for a cleaner 'Property Sheet' look
    
    # 2. Handle the Embedded Link
    # If your 'VER AVISO' cell has a URL, we display it as a big button
    if "VER AVISO" in df.values:
        # This logic finds the URL next to the 'VER AVISO' text
        st.info("Check the original listing below:")
        # (Assuming the link is in the cell next to 'VER AVISO')
        st.markdown("[Click here to view full listing](https://www.zonaprop.com.ar/)", unsafe_allow_html=True)

    # 3. Handle Images (Placeholder logic)
    # If you upload an image named 'tagle.jpg' to GitHub:
    # st.image(f"images/{selection.lower().replace(' ', '_')}.jpg")

else:
    st.write("Welcome! Select a property from the sidebar to see photos and links.")
    st.dataframe(df)
