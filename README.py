import streamlit as st
import pandas as pd
import os
import base64

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# --- CSS REFINADO PARA IMAGEN PEQUEÑA Y RESPONSIVE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    /* Eliminar espacios en blanco superiores */
    .stApp { margin-top: -90px; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Reducimos el ancho máximo para que no se vea "enorme" en monitores grandes */
    .block-container {
        padding-top: 0rem !important;
        max-width: 500px !important; 
        margin: 0 auto !important;
    }

    /* Contenedor del Banner - ALTURA CONTROLADA */
    .hero-container {
        width: 100%;
        height: 180px; /* Altura fija reducida para escritorio */
        overflow: hidden;
        margin-bottom: 1rem;
        border-radius: 0 0 10px 10px;
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Recorta la imagen para llenar el espacio sin deformar */
        object-position: center; 
    }

    /* Ajustes para Móvil */
    @media (max-width: 640px) {
        .hero-container { 
            height: 130px; /* Aún más pequeña en celulares */
        }
        .stApp { margin-top: -70px; }
    }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 22px !important;
        color: #1a1a1a;
        text-align: center;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .texto-base {
        font-size: 12px !important;
        font-family: sans-serif !important;
        color: #444;
    }

    .stButton>button {
        height: 26px !important;
        font-size: 10px !important;
        border: 1px solid #d4af37 !important;
        background-color: transparent !important;
    }
    
    hr { margin: 5px 0 !important; opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS Y RENDERIZADO ---
@st.cache_data
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
        # Render de Imagen con Base64 para asegurar visibilidad local
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)
            
            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                fila = st.columns([1.5, 0.8, 1.2])
                with fila[0]: st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with fila[1]:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with fila[2]:
                    val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)
    else:
        # Vista de detalle (se mantiene igual)
        if st.button("← VOLVER"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        st.subheader(st.session_state.opcion_actual)
        st.table(diccionario_hojas[st.session_state.opcion_actual].dropna(how='all'))
