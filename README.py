import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS "FORCE" (Ancho fijo y prolijo)
st.markdown("""
    <style>
    /* LIMITADOR MAESTRO: Nada puede medir más de 350px */
    .stApp {
        max-width: 350px !important;
        margin: 0 auto !important;
    }
    
    /* Eliminar paddings excesivos */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* FORZAR COLUMNAS EN MÓVIL (No se apilan) */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Imagen prolija */
    [data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
    }

    /* Textos y botones miniatura */
    .tabla-texto {
        font-size: 11px !important;
        margin: 0 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .stButton>button {
        height: 22px !important;
        font-size: 10px !important;
        padding: 0 !important;
        width: 100% !important;
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
        # Imagen Home (Limitada por el ancho de 350px del CSS)
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png")
        
        st.markdown("<h3 style='text-align: center; font-size: 15px; margin: 5px 0;'>Panel de Control</h3>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado (Columnas fijas)
            c_h = st.columns([1, 0.7, 1.2])
            c_h[0].write("**Unidad**")
            c_h[1].write("**Ver**")
            c_h[2].markdown("<div style='text-align:right'>**Contacto**</div>", unsafe_allow_html=True)
            st.markdown("---")

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    # Fila (No se apila)
                    fila = st.columns([1, 0.7, 1.2])
                    
                    with fila[0]:
                        st.markdown(f"<p class='tabla-texto'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ir", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    
                    with fila[2]:
                        val_cont = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<p class='tabla-texto' style='text-align:right'>{val_cont}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        if st.button("← Volver"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        opcion = st.session_state.opcion_actual
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img)
else:
    st.error("Error en archivo Excel.")
