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

# 2. CONEXIÓN DIRECTA A GOOGLE SHEETS
# Eliminamos cualquier referencia a archivos .xlsx locales para evitar el error de conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. LISTA DE FICHAS REALES
# He restaurado las unidades según tu estructura de inversión
nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554", "Cabello 3501"]

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp { background-color: #fcfcfd; }
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DE NAVEGACIÓN (Session State)
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- VISTA HOME ---
if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.6, 1.4], gap="large")
    
    with col_img:
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        # El radio button ahora muestra tus 4 opciones principales
        seleccion = st.radio(
            "Seleccione Unidad para analizar:", 
            nombres_hojas,
            index=nombres_hojas.index(st.session_state.opcion_actual) if st.session_state.opcion_actual in nombres_hojas else 0
        )
        
        if seleccion != "HOME":
            if st.button(f"Abrir Ficha de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

# --- VISTA DE DETALLE (FICHA TÉCNICA) ---
else:
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.subheader(f"Análisis de Unidad: {opcion}")
    
    try:
        # CONEXIÓN CRÍTICA: Lee la pestaña que coincide con el nombre seleccionado
        df = conn.read(worksheet=opcion, ttl=0)
        
        if df is not None:
            # Mostramos el editor de datos para que puedas gestionar el flujo de dinero
            df_editado = st.data_editor(
                df, 
                use_container_width=True, 
                hide_index=True,
                key=f"editor_{opcion}"
            )
            
            if st.button("💾 Guardar cambios en Google Drive"):
                conn.update(worksheet=opcion, data=df_editado)
                st.success(f"Datos de {opcion} actualizados correctamente.")
                st.cache_data.clear()
                st.rerun()
    
    except Exception as e:
        st.error(f"Error de conexión: No se pudo encontrar la pestaña '{opcion}' en Google Sheets.")
        st.info("Asegúrate de que la pestaña en tu archivo de Google se llame exactamente igual.")
