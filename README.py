import streamlit as st
import pandas as pd
import os
import base64
import urllib.parse

# 1. CONFIGURACIÓN DE IDENTIDAD (EDITA ESTO)
# Cambia la URL_BASE_APP por la dirección que te da Streamlit al publicar.
# Cambia la URL_IMAGEN_PREVIEW por el link "Raw" de tu imagen en GitHub.
URL_BASE_APP = "https://inversiones-inmobiliarias.streamlit.app/"
URL_IMAGEN_PREVIEW = "https://github.com/leomartire/Opciones_Deptos/blob/deee0c02a8c18a8a702adf350ede44f2b27e4bf8/images/HOME.png"

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

# Meta Tags para que WhatsApp reconozca la imagen de vista previa
st.markdown(f"""
    <head>
    <meta property="og:title" content="Zeylicovich & Arzumanián | Cartera 2026">
    <meta property="og:description" content="Propiedades exclusivas y proyectos de Flipping en CABA.">
    <meta property="og:image" content="{https://github.com/leomartire/Opciones_Deptos/blob/deee0c02a8c18a8a702adf350ede44f2b27e4bf8/images/HOME.png">
    <meta property="og:url" content="{https://inversiones-inmobiliarias.streamlit.app/}">
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

# --- 6. ESTILOS CSS UNIFICADOS (Cormorant Garamond + Simetría) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
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

    /* BOTONES UNIFICADOS (38px de alto, 14px de fuente) */
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
    .stButton>button p { font-size: 14px !important; font-family: 'Cormorant Garamond', serif !important; margin: 0 !important; }

    .btn-whatsapp { background-color: #25D366 !important; color: white !important; }
    .boton-aviso { background-color: #e0e0e0 !important; color: #1a1a1a !important; margin-top: 10px; }

    .hero-container {
        width: 100%; border-radius: 0 0 10px 10px; background-color: #f4f1ea;
        overflow: hidden; margin-bottom: 1rem; display: flex; justify-content: center;
    }
    .hero-container img { width: 100%; height: auto; object-fit: contain; max-height: 280px; }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 24px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px;
    }
    
    .texto-home { 
        font-size: 17px !important; 
        font-family: 'Cormorant Garamond', serif !important; 
        color: #1a1a1a; margin: 0 !important; font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}

    # --- VISTA: HOME ---
    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

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
            num_ws = "5491168807566"
            unidad_url = urllib.parse.quote(nombre_hoja)
            link_ficha = f"{https://inversiones-inmobiliarias.streamlit.app/}?unidad={unidad_url}"
            msg_url = urllib.parse.quote(f"Hola! Me interesa esta propiedad: {link_ficha}")            
            st.markdown(f'<a href="https://wa.me/{num_ws}?text={msg_url}" target="_blank" class="btn-whatsapp">WhatsApp</a>', unsafe_allow_html=True)
