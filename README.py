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

# --- CSS DE PRECISIÓN PARA MÓVIL (SIN DESBORDE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    .stApp { margin-top: -95px; }

    .block-container {
        padding-top: 0rem !important;
        max-width: 450px !important; /* Aún más estrecho para control total */
        margin: 0 auto !important;
        padding-left: 5px !important;
        padding-right: 5px !important;
    }

    .hero-container {
        width: 100%;
        height: 160px; 
        overflow: hidden;
        margin-bottom: 0.5rem;
        border-radius: 0 0 10px 10px;
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
    }

    /* FORZADO DE FILA ÚNICA EXTREMO */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        padding: 0px 2px !important; /* Elimina espacio lateral entre columnas */
    }

    [data-testid="stHorizontalBlock"] {
        gap: 0px !important; /* Elimina el espacio entre columnas de Streamlit */
        align-items: center !important;
    }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 18px !important;
        color: #1a1a1a;
        text-align: center;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .texto-base {
        font-size: 10.5px !important; /* Fuente más pequeña para que entre todo */
        font-family: sans-serif !important;
        color: #444;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Botón micro */
    .stButton>button {
        height: 22px !important;
        min-height: 22px !important;
        padding: 0px !important;
        font-size: 9px !important;
        border: 1px solid #d4af37 !important;
        background-color: transparent !important;
        width: 100% !important;
    }
    
    hr { margin: 3px 0 !important; opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

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
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()
            st.markdown("<hr style='border: 0.5px solid #333; margin-bottom: 8px;'>", unsafe_allow_html=True)
            
            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                # Proporciones híper-ajustadas: [Mucho espacio, Poco para el botón, Medio para contacto]
                fila = st.columns([1.8, 0.7, 1.3]) 
                
                with fila[0]: 
                    st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with fila[1]:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with fila[2]:
                    val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)
    else:
        if st.button("← VOLVER"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        st.subheader(st.session_state.opcion_actual)
        st.table(diccionario_hojas[st.session_state.opcion_actual].dropna(how='all'))
