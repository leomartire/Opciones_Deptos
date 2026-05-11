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

# --- 6. ESTILOS CSS ---
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

    .subtitulo-h2 {
        font-size: 19px !important; color: #b8860b; text-transform: uppercase;
        letter-spacing: 1.2px; margin-top: 25px; margin-bottom: 10px;
        border-bottom: 1px solid rgba(184, 134, 11, 0.3);
    }

    .stButton>button {
        height: 38px !important; line-height: 38px !important; width: 100% !important;
        background-color: #e0e0e0 !important; color: #1a1a1a !important;
        font-family: 'Cormorant Garamond', serif !important; font-size: 14px !important; 
        font-weight: 600 !important; text-transform: uppercase !important; border-radius: 4px !important;
    }

    .hero-container { width: 100%; border-radius: 0 0 10px 10px; overflow: hidden; margin-bottom: 1rem; }
    .hero-container img { width: 100%; height: auto; }
    .titulo-elegante { font-size: 24px !important; color: #1a1a1a; text-align: center; text-transform: uppercase; margin-bottom: 15px; }
    .texto-home { font-size: 17px !important; color: #1a1a1a; margin: 0 !important; font-weight: 500; }
    .btn-whatsapp { background-color: #25D366 !important; color: white !important; display: block; text-align: center; padding: 10px; border-radius: 4px; text-decoration: none; font-weight: 600; }
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

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            # Estructura solicitada:
            # H2 en Fila 4 (idx 3) -> Items en filas 6,7,8,9 (idx 5,6,7,8)
            # H2 en Fila 11 (idx 10) -> Item en fila 13 (idx 12)
            # H2 en Fila 15 (idx 14) -> Item en fila 17 (idx 16)
            
            secciones = [
                {"h2": 3, "items": [5, 6, 7, 8]},
                {"h2": 10, "items": [12]},
                {"h2": 14, "items": [16]}
            ]

            for seccion in secciones:
                # Dibujar Título H2
                idx_h2 = seccion["h2"]
                if idx_h2 < len(df_home):
                    texto_titulo = str(df_home.iloc[idx_h2, 0]).strip()
                    if texto_titulo and texto_titulo.lower() != "nan":
                        st.markdown(f"<h2 class='subtitulo-h2'>{texto_titulo}</h2>", unsafe_allow_html=True)
                
                # Dibujar Filas de ese grupo
                for idx_item in seccion["items"]:
                    if idx_item < len(df_home):
                        row = df_home.iloc[idx_item]
                        val_raw = str(row[0]).strip() if pd.notnull(row[0]) else ""
                        
                        if val_raw and val_raw.lower() != "nan":
                            col1, col2, col3 = st.columns([1.8, 0.7, 1.2]) 
                            with col1: 
                                st.markdown(f"<p class='texto-home' style='line-height:38px;'>{val_raw}</p>", unsafe_allow_html=True)
                            with col2:
                                if st.button("VER", key=f"btn_{idx_item}"):
                                    nombre_final = hojas_reales.get(val_raw.upper(), val_raw)
                                    st.session_state.opcion_actual = nombre_final
                                    st.query_params["unidad"] = nombre_final
                                    st.rerun()
                            with col3:
                                val_cont = str(row[2]).strip() if len(row) > 2 else "-"
                                st.markdown(f"<p class='texto-home' style='text-align:right; line-height:38px;'>{val_cont}</p>", unsafe_allow_html=True)
                            st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    # --- VISTA: FICHA TÉCNICA ---
    else:
        opcion = st.session_state.opcion_actual
        nombre_hoja = hojas_reales.get(opcion.upper(), opcion)
        
        img_ficha = get_base64(f"images/{nombre_hoja}.png")
        if img_ficha:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_ficha}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>{nombre_hoja}</h1>", unsafe_allow_html=True)
        
        if nombre_hoja in diccionario_hojas:
            df_ficha = diccionario_hojas[nombre_hoja].copy()
            url_aviso = None
            for col in df_ficha.columns:
                mask = df_ficha[col].str.contains("http|www", na=False)
                if mask.any():
                    url_aviso = df_ficha.loc[mask, col].values[0]
                    df_ficha.loc[mask, col] = pd.NA 
                    break
            
            st.table(df_ficha.iloc[1:].dropna(how='all'))
            if url_aviso:
                st.markdown(f'<a href="{url_aviso}" target="_blank" class="boton-aviso">VER AVISO PUBLICADO</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_volver, col_ws = st.columns(2)
        with col_volver:
            if st.button("← VOLVER", key="btn_back"):
                st.session_state.opcion_actual = "HOME"
                st.query_params.clear()
                st.rerun()
        with col_ws:
            unidad_url = urllib.parse.quote(nombre_hoja)
            link_ficha = f"{URL_BASE_APP}?unidad={unidad_url}"
            msg_url = urllib.parse.quote(f"Mirá esta propiedad de Zeylicovich & Arzumanián: {link_ficha}")
            st.markdown(f'<a href="https://api.whatsapp.com/send?text={msg_url}" target="_blank" class="btn-whatsapp">COMPARTIR</a>', unsafe_allow_html=True)
