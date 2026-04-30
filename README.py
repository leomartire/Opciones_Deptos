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

# 2. CONEXIÓN ÚNICA A GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. LISTA COMPLETA DE FICHAS (Asegúrate de que el nombre sea IDÉNTICO al de la pestaña en Google)
# He incluido todas las que mencionaste en tus versiones anteriores
nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554", "Cabello 3501", "Aviso"]

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

# 4. LÓGICA DE NAVEGACIÓN
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- VISTA HOME ---
if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.6, 1.4], gap="large")
    
    with col_img:
        # Solo intenta cargar la imagen si existe, no bloquea el resto
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        st.write("### Seleccione Unidad para analizar:")
        seleccion = st.radio(
            "Unidades Disponibles:", 
            nombres_hojas,
            label_visibility="collapsed"
        )
        
        if seleccion != "HOME":
            if st.button(f"🚀 Ver Detalle de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

# --- VISTA DE DETALLE (FICHA TÉCNICA) ---
else:
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.subheader(f"Análisis: {opcion}")
    
    try:
        # LEER DATOS DIRECTAMENTE DE LA PESTAÑA SELECCIONADA
        # worksheet=opcion le dice a Google qué pestaña abrir
        df = conn.read(worksheet=opcion, ttl=0)
        
        if df is not None:
            # Mostramos el editor de datos
            df_editado = st.data_editor(
                df, 
                use_container_width=True, 
                hide_index=True,
                key=f"editor_{opcion}"
            )
            
            # Botón para guardar cambios
            if st.button("💾 Guardar cambios en la nube"):
                conn.update(worksheet=opcion, data=df_editado)
                st.success("¡Datos actualizados correctamente en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
        else:
            st.error("No se pudieron recuperar datos de esta pestaña.")

    except Exception as e:
        st.error(f"Error de conexión con la pestaña '{opcion}'")
        st.info("Revisa que en tu archivo de Google Sheets la pestaña se llame exactamente igual (ojo con los espacios al final).")
