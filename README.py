import streamlit as st
import pandas as pd
import os
import base64
import urllib.parse

# 1. CONFIGURACIÓN DE IDENTIDAD Y PREVENTA 2026
URL_BASE_APP = "https://inversiones-inmobiliarias.streamlit.app/"
URL_IMAGEN_PREVIEW = "https://raw.githubusercontent.com/leomartire/Opciones_Deptos/main/images/HOME.png?v=2"

# 2. FUNCIÓN PARA PROCESAR IMÁGENES LOCALES
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 3. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# Meta Tags para WhatsApp
st.markdown(f"""
    <head>
    <meta property="og:title" content="Zeylicovich & Arzumanián | Inversiones">
    <meta property="og:description" content="Propiedades exclusivas y proyectos de Flipping en CABA.">
    <meta property="og:image" content="{URL_IMAGEN_PREVIEW}">
    <meta property="og:url" content="{URL_BASE_APP}">
    <meta property="og:type" content="website">
    </head>
    """, unsafe_allow_html=True)

# --- 4. CARGA DE DATOS ---
@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

# --- 5. LÓGICA DE NAVEGACIÓN ---
if "unidad" in st.query_params:
    st.session_state.opcion_actual = st.query_params["unidad"]
elif "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- 6. ESTILOS CSS + CARTEL DE ROTACIÓN + OCULTAR MENÚS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton { display: none !important; }
    
    #landscape-notice {
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #f4f1ea;
        color: #1a1a1a;
        z-index: 99999;
        text-align: center;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: 'Cormorant Garamond', serif;
        padding: 20px;
    }

    @media only screen and (max-width: 768px) and (orientation: portrait) {
        #landscape-notice { display: flex; }
    }

    .notice-icon { font-size: 50px; color: #b8860b; margin-bottom: 15px; }
    .notice-text { font-size: 20px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; line-height: 1.2; }

    .stApp { margin-top: -70px; } 
    .block-container {
        padding-top: 2rem !important; max-width: 450px !important; 
        margin: 0 auto !important; padding-left: 10px !important; padding-right: 10px !important;
    }
    
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Cormorant Garamond', serif !important;
    }

    .stTable td {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 15px !important;
        color: #444 !important;
    }

    thead, tbody th { display: none !important; }

    .stButton>button, .btn-whatsapp, .boton-aviso {
        height: 38px !important; 
        line-height: 38px !important;
        width: 100% !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 14px !important; 
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        border-radius: 4px !important;
        border: none !important;
        display: block !important;
        text-align: center !important;
        text-decoration: none !important;
        padding: 0 !important;
    }

    .stButton>button { background-color: #e0e0e0 !important; color: #1a1a1a !important; }
    .btn-whatsapp { background-color: #25D366 !important; color: white !important; }
    .boton-aviso { background-color: #e0e0e0 !important; color: #1a1a1a !important; margin-top: 10px; }

    .hero-container {
        width: 100%; border-radius: 0 0 10px 10px; background-color: #f4f1ea;
        overflow: hidden; margin-bottom: 1rem; display: flex; justify
