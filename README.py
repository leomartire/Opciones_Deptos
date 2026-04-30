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

# 2. CONEXIÓN (Sin carga automática para evitar errores al inicio)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTA DE TUS FICHAS (Agrégalas aquí exactamente como se llaman en Google) ---
# Si te falta alguna, solo agrégala a esta lista entre comillas y una coma.
nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554", "Cabello 3501", "Aviso"]

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

# 3. LÓGICA DE NAVEGACIÓN
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- VISTA HOME ---
if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.5, 1.5], gap="large")
    
    with col_img:
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        # El menú siempre tendrá todas las fichas de la lista 'nombres_hojas'
        seleccion = st.radio("Seleccione Unidad:", nombres_hojas)
        if seleccion != "HOME":
            if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

# --- VISTA DE FICHA TÉCNICA ---
else:
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.subheader(f"Análisis: {opcion}")
    
    try:
        # Aquí es donde intentamos la conexión específica a esa pestaña
        # Usamos ttl=0 para que siempre traiga el dato más nuevo
        df_actual = conn.read(worksheet=opcion, ttl=0)
        
        if df_actual is not None and not df_actual.empty:
            # Quitamos filas o columnas totalmente vacías para que se vea limpio
            df_clean = df_actual.dropna(how='all').dropna(axis=1, how='all')
            
            # Editor de datos
            df_editado = st.data_editor(df_clean, use_container_width=True, hide_index=True)
            
            if st.button("💾 Guardar cambios"):
                conn.update(worksheet=opcion, data=df_editado)
                st.success("¡Cambios guardados en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
        else:
            st.warning(f"La pestaña '{opcion}' parece estar vacía.")
            
    except Exception as e:
        st.error(f"Error de conexión con la pestaña '{opcion}'.")
        st.info("Asegúrate de que el nombre de la pestaña en Google Sheets sea EXACTAMENTE igual (mayúsculas, minúsculas y espacios).")
