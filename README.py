import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", # Cambiado a wide para que la imagen pueda expandirse
    page_icon="🏢"
)

# 2. ESTILO CSS CONSOLIDADO
st.markdown("""
    <style>
    /* Importar fuente elegante */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    /* Contenedor principal limitado para lectura cómoda */
    .block-container {
        padding-top: 0rem !important;
        max-width: 800px !important; 
        margin: 0 auto !important;
    }

    /* Imagen Principal (Hero) - SOLUCIÓN AL ENCUADRE */
    .hero-container {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        height: 350px; /* Altura fija para PC */
        overflow: hidden;
        margin-bottom: 2rem;
        background-color: #f4f1ea; /* Color hueso de fondo */
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Asegura que cubra todo sin deformarse */
        object-position: center; /* Centra la imagen */
    }

    /* Tipografía y Estilo de Texto */
    .texto-base {
        font-size: 13px !important;
        font-weight: 400 !important;
        font-family: 'Helvetica Neue', sans-serif !important;
        color: #444;
    }
    
    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 28px !important;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Botones Minimalistas */
    .stButton>button {
        height: 28px !important;
        padding: 0px 10px !important;
        font-size: 12px !important;
        border: 1px solid #d4af37 !important; /* Borde dorado sutil */
        color: #1a1a1a !important;
        background-color: transparent !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #d4af37 !important;
        color: white !important;
    }

    /* Esconder elementos de Streamlit por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
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
        # IMAGEN HERO RECTIFICADA
        if os.path.exists("images/HOME.png"):
            st.markdown(f"""
                <div class="hero-container">
                    <img src="https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/images/HOME.png" alt="Hero">
                </div>
                """, unsafe_allow_html=True)
            # NOTA: Si corres local, usa st.image("images/HOME.png", use_container_width=True) 
            # pero el CSS de arriba es mejor para la web desplegada.
        
        st.markdown("<h1 class='titulo-elegante'>Portfolio de Inversiones CABA 2026</h1>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado
            st.markdown("<hr style='border: 0.1px solid #ddd;'>", unsafe_allow_html=True)
            h = st.columns([1.5, 1, 1.2])
            h[0].markdown("<p class='texto-base' style='color:#888;'>PROPIEDAD</p>", unsafe_allow_html=True)
            h[1].markdown("<p class='texto-base' style='text-align:center; color:#888;'>DETALLES</p>", unsafe_allow_html=True)
            h[2].markdown("<p class='texto-base' style='text-align:right; color:#888;'>CONTACTO</p>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 0.5px solid #1a1a1a; margin-top: 0;'>", unsafe_allow_html=True)

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    fila = st.columns([1.5, 1, 1.2])
                    with fila[0]:
                        st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                    with fila[1]:
                        if st.button("Explorar", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        st.markdown(f"<h2 class='titulo-elegante'>{opcion}</h2>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)
else:
    st.error("No se encontró el archivo de datos Opciones_Deptos_LM.xlsx")
