import streamlit as st
import pandas as pd
import os
import base64

# 1. CARGA DE IMÁGENES
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. CONFIGURACIÓN
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# 3. CSS REFINADO (Gris Hueso, Dorado y Letra Negra)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');
    
    /* ADVERTENCIA MÓVIL */
    .orientacion-mensaje {
        display: none; background-color: #1a1a1a; color: #d4af37;
        text-align: center; padding: 15px; font-family: sans-serif;
        font-weight: bold; font-size: 13px; border-bottom: 2px solid #d4af37;
        width: 100%; position: fixed; top: 0; left: 0; z-index: 999999;
    }
    @media only screen and (max-width: 900px) and (orientation: portrait) {
        .orientacion-mensaje { display: block !important; }
    }

    /* ESTRUCTURA */
    .stApp { margin-top: -70px; } 
    .block-container {
        padding-top: 2rem !important; max-width: 450px !important; 
        margin: 0 auto !important; padding-left: 10px !important; padding-right: 10px !important;
    }
    
    thead, tbody th { display: none !important; }

    /* --- UNIFICACIÓN TOTAL DE BOTONES (Altura 32px) --- */
    
    .stButton>button {
        height: 32px !important; 
        width: 100% !important;
        font-size: 10px !important; 
        border-radius: 4px !important;
        font-family: sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 !important;
        transition: background-color 0.3s ease;
    }

    /* Botón VER (Dorado con Letra Negra) */
    div.stButton > button {
        background-color: #d4af37 !important;
        color: #1a1a1a !important;
    }

    /* Botón VOLVER (Gris Claro / Hueso con Letra Negra) */
    div.stButton > button[kind="secondary"] {
        background-color: #e0e0e0 !important; /* Gris claro elegante */
        color: #1a1a1a !important;
        border: 1px solid #cccccc !important;
    }

    /* Botón WhatsApp (Verde con Altura Sincronizada) */
    .btn-whatsapp {
        height: 32px !important;
        background-color: #25D366 !important;
        color: white !important;
        text-align: center;
        line-height: 32px !important;
        border-radius: 4px;
        font-family: sans-serif;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-decoration: none;
        display: block;
        width: 100%;
    }

    /* CONTENEDORES DE IMAGEN */
    .hero-container-home, .hero-container-ficha {
        width: 100%; border-radius: 0 0 10px 10px; background-color: #f4f1ea;
        overflow: hidden; margin-bottom: 1rem; display: flex; justify-content: center;
    }
    .hero-container-home { height: auto; min-height: 100px; }
    .hero-container-home img { width: 100%; height: auto; object-fit: contain; }
    .hero-container-ficha { height: auto; max-height: 280px; }
    .hero-container-ficha img { max-width: 100%; max-height: 280px; object-fit: contain; }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;
    }
    .texto-base { font-size: 11px !important; font-family: sans-serif !important; color: #444; margin: 0 !important; }

    /* BOTÓN VER AVISO */
    .boton-aviso {
        display: block; width: 100%; text-align: center;
        background-color: #fdfcf9; color: #1a1a1a; 
        border: 1px solid #d4af37;
        padding: 10px 0; border-radius: 4px;
        font-size: 11px; text-decoration: none; font-family: sans-serif;
        margin-top: 10px; font-weight: 600; text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    
    <div class="orientacion-mensaje">
        🔄 POR FAVOR, GIRE SU PANTALLA (MODO APAISADO)
    </div>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container-home"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            unidades_vistas = set()
            st.markdown("<hr style='margin: 0 0 8px 0; opacity: 0.3; border-top: 1px solid #333;'>", unsafe_allow_html=True)
            for index, row in df_home.iterrows():
                val_raw = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if (not val_raw or val_raw.upper() in ["UNIDAD", "HOME"] or val_raw.isdigit() or val_raw in unidades_vistas):
                    continue
                unidades_vistas.add(val_raw)
                
                col1, col2, col3 = st.columns([1.9, 0.7, 1.1]) 
                with col1: 
                    st.markdown(f"<p class='texto-base' style='line-height:32px;'>{val_raw}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_raw.upper(), "HOME")
                        st.rerun()
                with col3:
                    val_cont = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right; line-height:32px;'>{val_cont}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    else:
        opcion = st.session_state.opcion_actual
        img_ficha = get_base64(f"images/{opcion}.png")
        if img_ficha:
            st.markdown(f'<div class="hero-container-ficha"><img src="data:image/png;base64,{img_ficha}"></div>', unsafe_allow_html=True)
        st.markdown(f"<h1 class='titulo-elegante'>{opcion}</h1>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].copy()
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
            if st.button("← VOLVER", key="btn_back", type="secondary"):
                st.session_state.opcion_actual = "HOME"
                st.rerun()
        
        with col_ws:
            num_ws = "5491168807566"
            txt_ws = f"Hola! Me interesa obtener más información sobre: {opcion}"
            link_ws = f"https://wa.me/{num_ws}?text={txt_ws.replace(' ', '%20')}"
            st.markdown(f'<a href="{link_ws}" target="_blank" class="btn-whatsapp">WhatsApp</a>', unsafe_allow_html=True)
