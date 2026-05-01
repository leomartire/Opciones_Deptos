import streamlit as st
import pandas as pd
import os
import base64

# 1. FUNCIÓN PARA CARGAR IMÁGENES LOCALES (Evita el error de "Imagen no disponible")
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# 3. ESTILO CSS CONSOLIDADO (Móvil, Desktop y Estética Minimalista)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    /* Eliminar el espacio superior innecesario de Streamlit */
    .stApp { margin-top: -75px; }
    header { visibility: hidden; }

    /* Contenedor de contenido centralizado */
    .block-container {
        padding-top: 0rem !important;
        max-width: 600px !important; 
        margin: 0 auto !important;
    }

    /* Banner Principal: Altura reducida para mejor visibilidad */
    .hero-container {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        height: 220px; 
        overflow: hidden;
        background-color: #f4f1ea;
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
        object-position: center;
    }

    /* Tipografía de autor */
    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 24px !important;
        color: #1a1a1a;
        text-align: center;
        margin: 1.5rem 0 0.5rem 0;
        letter-spacing: 1px;
    }

    .texto-base {
        font-size: 12px !important;
        font-family: 'Helvetica Neue', Helvetica, sans-serif !important;
        color: #444;
        margin: 0 !important;
    }

    /* Botones Minimalistas */
    .stButton>button {
        height: 28px !important;
        width: 100% !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #d4af37 !important;
        background-color: transparent !important;
        border-radius: 4px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #d4af37 !important;
        color: white !important;
    }

    /* Ajustes específicos para móviles */
    @media (max-width: 640px) {
        .hero-container { height: 160px; }
        .titulo-elegante { font-size: 20px !important; }
        [data-testid="column"] {
            flex: 1 1 0% !important;
            min-width: 0px !important;
        }
    }

    hr { margin: 8px 0 !important; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS (Excel)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        # Cargamos todas las hojas del Excel
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

# 5. LÓGICA DE NAVEGACIÓN Y VISTAS
if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # Imagen Banner
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>PORTFOLIO DE INVERSIONES 2026</h1>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado de Tabla
            st.markdown("<hr style='border: 0.5px solid #1a1a1a; margin-bottom:10px;'>", unsafe_allow_html=True)
            h = st.columns([1.5, 0.8, 1.2])
            h[0].markdown("<p class='texto-base' style='color:#888;'>UNIDAD</p>", unsafe_allow_html=True)
            h[1].markdown("<p class='texto-base' style='text-align:center; color:#888;'>ACCIÓN</p>", unsafe_allow_html=True)
            h[2].markdown("<p class='texto-base' style='text-align:right; color:#888;'>CONTACTO</p>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                # Filtramos nombres de hojas y vacíos
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                fila = st.columns([1.5, 0.8, 1.2])
                with fila[0]:
                    st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with fila[1]:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with fila[2]:
                    val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← VOLVER"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        st.markdown(f"<h2 class='titulo-elegante'>{opcion}</h2>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
            
            # Imagen de la propiedad específica
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)
else:
    st.error("No se pudo cargar el archivo Excel. Verifique que 'Opciones_Deptos_LM.xlsx' esté en la raíz.")
