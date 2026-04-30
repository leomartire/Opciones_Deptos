import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="centered", 
    page_icon="🏢"
)

# 2. ESTILO CSS CONSOLIDADO (Logo centrado, fuente unificada, sin negritas)
st.markdown("""
    <style>
    /* Contenedor principal */
    .block-container {
        padding-top: 1rem !important;
        max-width: 550px !important; 
        margin: 0 auto !important;
    }

    /* Logo: Forzar centrado absoluto */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 20px;
    }

    /* Tipografía unificada: Sin negritas, mismo tamaño (12px) */
    .texto-base {
        font-size: 12px !important;
        font-weight: 400 !important;
        font-family: sans-serif !important;
        margin: 0 !important;
        line-height: 1.5;
        color: #333;
    }

    /* Forzar que las columnas no se apilen en móvil */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Botones minimalistas */
    .stButton>button {
        height: 26px !important;
        padding: 0px 5px !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        min-height: 26px !important;
        width: 100% !important;
        border: 1px solid #ccc;
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
        # Logo Centrado (320px)
        if os.path.exists("images/HOME.png"):
            col_izq, col_logo, col_der = st.columns([1, 4, 1])
            with col_logo:
                st.image("images/HOME.png", width=320)
        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado unificado (Sin negritas)
            st.markdown("---")
            h = st.columns([1, 0.8, 1.2])
            h[0].markdown("<p class='texto-base'>Unidad</p>", unsafe_allow_html=True)
            h[1].markdown("<p class='texto-base' style='text-align:center;'>Acción</p>", unsafe_allow_html=True)
            h[2].markdown("<p class='texto-base' style='text-align:right;'>Contacto</p>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 0.5px solid #666; margin: 2px 0;'>", unsafe_allow_html=True)

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    # Fila unificada (Misma fuente y tamaño)
                    fila = st.columns([1, 0.8, 1.2])
                    
                    with fila[0]:
                        st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

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
