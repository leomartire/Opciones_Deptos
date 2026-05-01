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
    <meta property="og:title" content="Zeylicovich & Arzumanián | Inversines Mayo 2026">
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

# --- 6. ESTILOS CSS + CARTEL DE ROTACIÓN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
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
        overflow: hidden; margin-bottom: 1rem; display: flex; justify-content: center;
    }
    .hero-container img { width: 100%; height: auto; object-fit: contain; max-height: 280px; }

    .titulo-elegante {
        font-size: 24px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px;
    }
    
    .texto-home { 
        font-size: 17px !important; color: #1a1a1a; margin: 0 !important; font-weight: 500;
    }
    </style>

    <div id="landscape-notice">
        <div class="notice-icon">🔄</div>
        <div class="notice-text">Zeylicovich & Arzumanián<br><br>Por favor, gire su dispositivo para una mejor experiencia.</div>
    </div>
    """, unsafe_allow_html=True)

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}

    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Listado de opciones</h1>", unsafe_allow_html=True)

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
            # LÓGICA COMPARTIR GENÉRICA (SIN TELÉFONO)
            unidad_url = urllib.parse.quote(nombre_hoja)
            link_ficha = f"{URL_BASE_APP}?unidad={unidad_url}&r=2026"
            msg_url = urllib.parse.quote(f"Mirá esta propiedad de Zeylicovich & Arzumanián: {link_ficha}")
            
            # Al no poner número después de 'send', WhatsApp abre la lista de contactos
            st.markdown(f'<a href="https://api.whatsapp.com/send?text={msg_url}" target="_blank" class="btn-whatsapp">COMPARTIR</a>', unsafe_allow_html=True)
