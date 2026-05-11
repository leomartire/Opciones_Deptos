import streamlit as st
import pandas as pd
import os
import base64

# --- CONFIGURACIÓN Y ESTILOS (Se mantienen igual) ---
st.set_page_config(page_title="Zeylicovich & Arzumanián | Inversiones", layout="wide")

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, div { font-family: 'Cormorant Garamond', serif !important; }
    .titulo-elegante { font-size: 26px; color: #1a1a1a; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }
    .subtitulo-h2 { font-size: 20px; color: #b8860b; text-transform: uppercase; margin-top: 35px; border-bottom: 1px solid rgba(184,134,11,0.3); }
    .texto-home { font-size: 17px; color: #1a1a1a; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

# --- NAVEGACIÓN ---
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if st.session_state.opcion_actual == "HOME":
        # Hero Image
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{img_64}" style="width:100%; max-height:250px; object-fit:cover;"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Portafolio de Activos Estratégicos 2026</h1>", unsafe_allow_html=True)

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            # Mapeo de jerarquía según tu indicación (Ajustado a índice 0 de Python: fila 4 -> index 3)
            # h2_indices: 3 (Fila 4), 10 (Fila 11), 14 (Fila 15)
            # pertenencias: {3: [5,6,7,8], 10: [12], 14: [16]} -> (Índices de fila Excel - 1)
            
            secciones = [
                {"titulo_idx": 3, "items_idxs": [5, 6, 7, 8]},
                {"titulo_idx": 10, "items_idxs": [12]},
                {"titulo_idx": 14, "items_idxs": [16]}
            ]

            for seccion in secciones:
                # Renderizar el H2 (Fila de título)
                idx_h2 = seccion["titulo_idx"]
                if idx_h2 < len(df_home):
                    texto_h2 = str(df_home.iloc[idx_h2, 0]).strip()
                    st.markdown(f"<h2 class='sub
