import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. INICIALIZAR CONEXIÓN (Única fuente de datos)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', sans-serif !important;
        color: #1e293b;
    }
    .stApp { background-color: #fcfcfd; }
    h1 { font-size: 1.6rem !important; font-weight: 600 !important; color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. LISTA DE UNIDADES (Sustituye a la antigua carga de Excel)
# Agrega aquí todas las pestañas que tengas en tu Google Sheet
nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554", "Cabello 3501"]

if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# 4. LÓGICA DE NAVEGACIÓN
if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.5, 1.5], gap="large")
    
    with col_img:
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        seleccion = st.radio(
            "Seleccione Unidad:", 
            nombres_hojas, 
            index=nombres_hojas.index(st.session_state.opcion_actual) if st.session_state.opcion_actual in nombres_hojas else 0
        )
        
        if seleccion != "HOME":
            if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

else:
    # --- VISTA DE DETALLE (LECTURA DESDE LA NUBE) ---
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.markdown(f"<h1>Análisis: {opcion}</h1>", unsafe_allow_html=True)
    
    # Determinamos la hoja a cargar (Mantenemos tu lógica de 'Aviso' para Tagle)
    hoja_a_cargar = "Aviso" if (opcion == "Tagle 2554") else opcion
    
    col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
    
    with col_main:
        st.subheader("Ficha Técnica (Google Sheets)")
        
        try:
            # LEER DIRECTAMENTE DE LA NUBE
            df_actual = conn.read(worksheet=hoja_a_cargar.strip(), ttl=0)
            
            if not df_actual.empty:
                # Limpieza de nulos para la vista
                df_clean = df_actual.dropna(how='all', axis=0).dropna(how='all', axis=1)
                
                # EDITOR DE DATOS
                df_editado = st.data_editor(
                    df_clean, 
                    use_container_width=True, 
                    hide_index=True,
                    key=f"editor_{hoja_a_cargar}"
                )
                
                if st.button("💾 Guardar cambios en Drive"):
                    conn.update(worksheet=hoja_a_cargar.strip(), data=df_editado)
                    st.success("¡Sincronizado con éxito!")
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.warning("La pestaña está vacía.")
                
        except Exception as e:
            st.error(f"Error: No se encontró la pestaña '{hoja_a_cargar}' en Google Sheets.")
            st.info("Verifica que el nombre coincida exactamente en tu Drive.")

    with col_gallery:
        st.subheader("Galería")
        st.info(f"Contenido de {opcion}")
