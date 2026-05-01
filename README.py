import streamlit as st
import pandas as pd
import os
import base64

# 1. FUNCIÓN PARA LEER IMAGEN LOCAL Y CONVERTIRLA A BASE64
# Esto permite que el HTML de Streamlit "vea" tu archivo local
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# 3. ESTILO CSS CONSOLIDADO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    .block-container {
        padding-top: 0rem !important;
        max-width: 800px !important; 
        margin: 0 auto !important;
    }

    /* Contenedor del Banner */
    .hero-container {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        height: 350px; 
        overflow: hidden;
        margin-bottom: 2rem;
        background-color: #f4f1ea;
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
        object-position: center;
    }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 28px !important;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1rem;
    }

    .texto-base {
        font-size: 13px !important;
        font-family: sans-serif !important;
        color: #444;
    }

    .stButton>button {
        height: 28px !important;
        font-size: 12px !important;
        border: 1px solid #d4af37 !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
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

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # RENDERIZADO DE IMAGEN LOCAL
        ruta_home = "images/HOME.png"
        if os.path.exists(ruta_home):
            img_base64 = get_base64_of_bin_file(ruta_home)
            st.markdown(f"""
                <div class="hero-container">
                    <img src="data:image/png;base64,{img_base64}">
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Portfolio de Inversiones CABA 2026</h1>", unsafe_allow_html=True)

        # ... (Resto del código de las tablas igual que antes)
        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()
            st.markdown("<hr style='border: 0.1px solid #ddd;'>", unsafe_allow_html=True)
            h = st.columns([1.5, 1, 1.2])
            h[0].markdown("<p class='texto-base' style='color:#888;'>PROPIEDAD</p>", unsafe_allow_html=True)
            h[1].markdown("<p class='texto-base' style='text-align:center; color:#888;'>DETALLES</p>", unsafe_allow_html=True)
            h[2].markdown("<p class='texto-base' style='text-align:right; color:#888;'>CONTACTO</p>", unsafe_allow_html=True)
            
            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"]: continue
                    if val_unidad in unidades_vistas: continue
                    unidades_vistas.add(val_unidad)
                    
                    fila = st.columns([1.5, 1, 1.2])
                    with fila[0]: st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                    with fila[1]:
                        if st.button("Explorar", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                        st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        st.markdown(f"<h2 class='titulo-elegante'>{opcion}</h2>", unsafe_allow_html=True)
        if opcion in diccionario_hojas:
            st.table(diccionario_hojas[opcion].dropna(how='all'))
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)
