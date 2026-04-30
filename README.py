import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CONEXIÓN Y DATOS
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=0)
def cargar_nombres_hojas():
    try:
        # Traemos los datos para identificar las pestañas
        df = conn.read()
        # Si el archivo tiene pestañas, Google nos suele dar acceso a ellas
        # Aquí definimos manualmente las que tienes en tu Sheet para que no desaparezcan
        return ["HOME", "Lafinur 3000", "Tagle 2554", "Cabello 3501"] 
    except:
        return ["HOME"]

nombres_hojas = cargar_nombres_hojas()

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp { background-color: #fcfcfd; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.5, 1.5], gap="large")
    
    with col_img:
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        seleccion = st.radio("Seleccione Unidad:", nombres_hojas)
        if seleccion != "HOME":
            if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

else:
    # --- VISTA DE FICHA TÉCNICA ---
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.subheader(f"Análisis: {opcion}")
    
    try:
        # Leemos la pestaña de Google Sheets
        df_actual = conn.read(worksheet=opcion, ttl=0)
        
        if df_actual is not None:
            # Editor de datos simple
            df_editado = st.data_editor(df_actual, use_container_width=True, hide_index=True)
            
            if st.button("💾 Guardar cambios"):
                conn.update(worksheet=opcion, data=df_editado)
                st.success("Guardado")
                st.cache_data.clear()
                st.rerun()
    except Exception as e:
        st.error("Error al cargar la ficha. Verifica que el nombre de la pestaña en Google sea idéntico.")
