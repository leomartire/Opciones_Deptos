import streamlit as st
import pandas as pd

st.set_page_config(page_title="Property Comparison", layout="wide")

# 1. THE INDEX (The 'HOME' sheet)
# We load your main list of apartments here
@st.cache_data
def load_data():
    # In a real scenario, this loads your uploaded Excel
    return pd.read_excel("Opciones_Deptos.xlsx", sheet_name=None)

sheets = load_data()

# 2. SIDEBAR NAVIGATION
st.sidebar.title("🏙️ Apartment Index")
selection = st.sidebar.selectbox("Select a Property:", list(sheets.keys()))

# 3. CONTENT REDIRECTION
st.title(f"Details for: {selection}")

df = sheets[selection]

# Display key metrics (Price, M2, etc.) if they exist in your data
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    # Simple search within the selected tab
    search = st.text_input("Filter details:")
    if search:
        filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.write(filtered_df)
else:
    st.info("Select a property from the sidebar to see the breakdown.")