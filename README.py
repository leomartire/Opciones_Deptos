import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', sans-serif !important;
        color: #1e293b;
    }
    .stApp { background-color: #fcfcfd; }
    h1 { font-size: 2.2rem !important; font-weight: 600 !important; color: #0f172a !important; }
    h2 { font-size: 1.4rem !important; color: #334155 !important; font-weight: 500 !important; }
    
    .stRadio [data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CAPA DE DATOS (Basada en tu archivo .xlsx)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos todas las hojas del Excel
            return pd.read_excel(archivo, sheet_name=None)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        
        # --- COLUMNAS PARA IMAGEN Y MENÚ ---
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
            else:
                st.warning("Imagen 'HOME.png' no encontrada")
        
        with col_menu:
            seleccion = st.radio(
                "Seleccione Unidad:", 
                nombres_hojas, 
                index=nombres_hojas.index("HOME") if "HOME" in nombres_hojas else 0
            )
            
            if seleccion != "HOME":
                if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                    st.session_state.opcion_actual = seleccion
                    st.rerun()

    else:
        # --- VISTA DE DETALLE DE PROPIEDAD ---
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        titulo_limpio = opcion.replace("HOME", "").strip()
        st.markdown(f"<h1 style='font-size: 1.6rem !important;'>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df = diccionario_hojas[opcion]
            
            # Limpieza básica para visualización
            df_clean = df.dropna(how='all').dropna(axis=1, how='all')
            
            col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
            
            with col_main:
                st.subheader("Ficha Técnica")
                st.dataframe(df_clean, use_container_width=True, hide_index=True)
                
                # Buscador de links en la ficha
                for val in df_clean.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        st.link_button("🌐 Ver Publicación Original", txt, use_container_width=True)
        else:
            st.error("No se encontró la información de la hoja seleccionada.")
else:
    st.error("No se encontró el archivo 'Opciones_Deptos_LM.xlsx'. Asegúrate de que esté en la carpeta principal.")
