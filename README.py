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

# --- 6. ESTILOS CSS GENERALES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton { display: none !important; }
    
    .stApp { margin-top: -70px; } 
    .block-container {
        padding-top: 2rem !important; max-width: 450px !important; 
        margin: 0 auto !important; padding-left: 10px !important; padding-right: 10px !important;
    }
    
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Cormorant Garamond', serif !important;
    }

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
        overflow: hidden; margin-bottom: 1rem; display: flex; justify-content: center;
    }
    .hero-container img { width: 100%; height: auto; object-fit: contain; max-height: 280px; }

    .titulo-elegante {
        font-size: 24px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px;
    }
    
    .subtitulo-h2 {
        font-size: 19px !important; color: #b8860b; text-transform: uppercase;
        letter-spacing: 1.2px; margin-top: 25px; margin-bottom: 5px;
        border-bottom: 1px solid rgba(184, 134, 11, 0.3);
    }
    .descripcion-h2 {
        font-size: 15px; color: #555; font-style: italic; margin-bottom: 15px; line-height: 1.2;
    }

    .texto-home { font-size: 17px !important; color: #1a1a1a; margin: 0 !important; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}

    # --- VISTA: HOME ---
    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Listado de opciones</h1>", unsafe_allow_html=True)

        # 1) Pendientes de visita LF y LC
        st.markdown("<h2 class='subtitulo-h2'>1) Pendientes de visita LF y LC</h2>", unsafe_allow_html=True)
        st.markdown("<p class='descripcion-h2'>Unidades identificadas en el radar de inversión pendientes de validación técnica.</p>", unsafe_allow_html=True)

        # 2) Pendiente de visita Revaloriza
        st.markdown("<h2 class='subtitulo-h2'>2) Pendiente de visita Revaloriza</h2>", unsafe_allow_html=True)
        st.markdown("<p class='descripcion-h2'>Activos seleccionados bajo criterios de seguridad y plusvalía en proceso de auditoría física.</p>", unsafe_allow_html=True)

        # 3) Visitados continúan como opción de inversión
        st.markdown("<h2 class='subtitulo-h2'>3) Visitados continúan como opción de inversión</h2>", unsafe_allow_html=True)
        st.markdown("<p class='descripcion-h2'>Propiedades con inspección técnica superada y métricas de ROI confirmadas.</p>", unsafe_allow_html=True)

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            st.markdown("<hr style='margin: 0 0 8px 0; opacity: 0.3;'>", unsafe_allow_html=True)
            for index, row in df_home.iterrows():
                val_raw = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if not val_raw or val_raw.upper() in ["UNIDAD", "HOME"] or val_raw.isdigit():
                    continue
                
                col1, col2, col3 = st.columns([1.8, 0.7, 1.2]) 
                with col1: 
                    st.markdown(f"<p class='texto-home' style='line-height:38px;'>{val_raw}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_{index}"):
                        nombre_final = hojas_reales.get(val_raw.upper(), val_raw)
                        st.session_state.opcion_actual = nombre_final
                        st.query_params["unidad"] = nombre_final
                        st.rerun()
                with col3:
                    val_cont = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-home' style='text-align:right; line-height:38px;'>{val_cont}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)
