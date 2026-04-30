import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="centered", # Mantiene el contenido contenido en el centro
    page_icon="🏢"
)

# 2. ESTILO CSS PARA CONTROL DE TAMAÑOS (Logo grande, tabla compacta)
st.markdown("""
    <style>
    /* 1. Achicar márgenes superiores */
    /* 1. Contenedor principal */
    .block-container {
        padding-top: 1rem !important;
        max-width: 550px !important; 
        margin: 0 auto !important;
    }

    /* 2. LOGO: Forzar centrado total */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 20px;
    }

    /* 3. TIPOGRAFÍA UNIFICADA: Sin negritas, misma fuente */
    .tabla-texto, .contacto-texto, .encabezado-tabla {
        font-size: 12px !important;
        font-weight: 400 !important; /* Quita las negritas */
        font-family: sans-serif !important;
        margin: 0 !important;
        line-height: 1.5;
    }

    /* 3. EVITAR QUE LAS COLUMNAS SE APILEN EN MÓVIL */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 4. Textos de tabla y Botones */
    .tabla-texto {
        font-size: 12px !important;
        margin: 0 !important;
        line-height: 1.5;
    }

    .stButton>button {
        height: 24px !important;
        padding: 0px 5px !important;
        font-size: 10px !important;
        min-height: 24px !important;
        width: 100% !important;
    }

    .contacto-texto {
        font-size: 12px !important;
        color: #555;
        text-align: right;
    }

    hr { margin: 6px 0 !important; opacity: 0.2; }
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
        if os.path.exists("images/HOME.png"):
            # Usamos columnas para forzar el centrado físico además del CSS
            col_izq, col_logo, col_der = st.columns([1, 4, 1])
            with col_logo:
                st.image("images/HOME.png", width=320)
        
        st.markdown("<p style='text-align: center; font-size: 14px; font-weight: 400;'>Panel de Control</p>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            # ... resto de tu código de carga ...
            
            # Encabezado Manual (Cambié <b> por <p> para quitar negritas)
            st.markdown("---")
            h = st.columns([1, 0.8, 1.2])
            h[0].markdown("<p class='encabezado-tabla'>Unidad</p>", unsafe_allow_html=True)
            h[1].markdown("<p class='encabezado-tabla' style='text-align:center;'>Acción</p>", unsafe_allow_html=True)
            h[2].markdown("<p class='encabezado-tabla' style='text-align:right;'>Contacto</p>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)
else:
    st.error("Error al cargar el archivo Excel.")
