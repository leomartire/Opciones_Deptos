import streamlit as st
import pandas as pd
import os
import base64

# 1. FUNCIÓN DE CARGA DE IMÁGENES (Unificada para Home y Fichas)
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

# 3. CSS CONSOLIDADO PARA TODA LA APP
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    /* Ajuste de margen superior para no tapar el botón Volver */
    .stApp { margin-top: -70px; }

    .block-container {
        padding-top: 0rem !important;
        max-width: 450px !important; 
        margin: 0 auto !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    /* Banners de Home y Fichas */
    .hero-container {
        width: 100%;
        height: 160px; 
        overflow: hidden;
        margin-bottom: 1rem;
        border-radius: 0 0 10px 10px;
        background-color: #f4f1ea;
    }
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
    }

    /* Tipografías unificadas */
    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important;
        color: #1a1a1a;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }

    .texto-base {
        font-size: 11px !important;
        font-family: sans-serif !important;
        color: #444;
    }

    /* Tablas de Ficha Técnica personalizadas */
    .stTable {
        font-size: 11px !important;
        font-family: sans-serif !important;
    }

    /* Botones (Ver y Volver) */
    .stButton>button {
        height: 26px !important;
        font-size: 10px !important;
        border: 1px solid #d4af37 !important;
        background-color: transparent !important;
        width: 100% !important;
        border-radius: 4px;
        color: #1a1a1a;
    }
    
    .stButton>button:hover {
        background-color: #d4af37 !important;
        color: white !important;
    }

    /* Forzado de fila en Home */
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; padding: 0px 2px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; align-items: center !important; }

    hr { margin: 4px 0 !important; opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

# 4. DATOS
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

    # --- NAVEGACIÓN ---
    
    # VISTA HOME
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
                
                fila = st.columns([1.8, 0.7, 1.3]) 
                with fila[0]: st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with fila[1]:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with fila[2]:
                    val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)

    # VISTA FICHA TÉCNICA
    else:
        opcion = st.session_state.opcion_actual
        
        # Imagen de la Unidad (Usando el mismo estilo que la Home)
        ruta_img = f"images/{opcion}.png"
        img_ficha_64 = get_base64(ruta_img)
        if img_ficha_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_ficha_64}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>Ficha: {opcion}</h1>", unsafe_allow_html=True)
        
        # Tabla de Datos
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón Volver (Ahora visible y estilizado)
        if st.button("← VOLVER AL PANEL"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

else:
    st.error("Error: Opciones_Deptos_LM.xlsx no encontrado.")
