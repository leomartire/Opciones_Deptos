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

# 2. INICIALIZAR CONEXIÓN
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

# 3. CARGA DINÁMICA DE TODAS LAS HOJAS
try:
    # Leemos el archivo completo para obtener los nombres de las pestañas
    # Nota: st-gsheets-connection devuelve un diccionario si no especificas 'worksheet'
    todas_las_hojas = conn.read(ttl=0)
    
    if isinstance(todas_las_hojas, dict):
        nombres_hojas = list(todas_las_hojas.keys())
    else:
        # Si devuelve un solo DataFrame, intentamos obtener metadatos o usamos una lista base
        nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554"] 

    # 4. LÓGICA DE NAVEGACIÓN
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
        
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
        # --- VISTA DE DETALLE ---
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.markdown(f"<h1>Análisis: {opcion}</h1>", unsafe_allow_html=True)
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            st.subheader("Ficha Técnica")
            
            # Leer la hoja específica seleccionada
            df_actual = conn.read(worksheet=opcion.strip(), ttl=0)
            
            if not df_actual.empty:
                # Limpiar columnas vacías y formatear
                df_viz = df_actual.dropna(how='all', axis=0).dropna(how='all', axis=1)
                
                # Editor de datos para guardar cambios
                df_editado = st.data_editor(
                    df_viz, 
                    use_container_width=True, 
                    hide_index=True,
                    key=f"editor_{opcion}"
                )
                
                if st.button("💾 Guardar cambios en Google Drive"):
                    conn.update(worksheet=opcion.strip(), data=df_editado)
                    st.success("¡Datos guardados!")
                    st.cache_data.clear()
                    st.rerun()
                
                # Links automáticos
                for val in df_actual.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        url = txt[txt.lower().find("http"):].split()[0]
                        st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)

        with col_gallery:
            st.subheader("Galería")
            st.info(f"Mostrando información de {opcion}")

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.info("Verifica que el ID en Secrets sea de un archivo 'Google Sheets' y no un '.xlsx'.")
