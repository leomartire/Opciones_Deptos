import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS (Control total de anchos y comportamiento móvil)
st.markdown("""
    <style>
    /* 1. Centrado para PC */
    @media (min-width: 1024px) {
        .block-container {
            max-width: 500px !important;
            margin: auto !important;
        }
    }

    /* 2. EVITAR QUE LAS COLUMNAS SE APILEN EN MÓVIL */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 3. Ajustes de espaciado y textos */
    .block-container {
        padding-top: 1rem !important;
    }

    .stButton>button {
        height: 24px !important;
        padding: 0px 5px !important;
        font-size: 11px !important;
        min-height: 24px !important;
        width: 100% !important;
    }

    .tabla-texto {
        font-size: 11px !important;
        margin: 0 !important;
        line-height: 1.5;
    }

    hr { margin: 4px 0 !important; opacity: 0.2; }
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
        # Usamos columnas para centrar la imagen y que no sea gigante
        c_img1, c_img2, c_img3 = st.columns([1, 1, 1])
        with c_img2:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        st.markdown("<h3 style='text-align: center; font-size: 18px; margin-top: 0;'>Panel de Control</h3>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado
            h = st.columns([1, 0.8, 1.2])
            h[0].markdown("<b style='font-size:11px;'>Unidad</b>", unsafe_allow_html=True)
            h[1].markdown("<center><b style='font-size:11px;'>Acción</b></center>", unsafe_allow_html=True)
            h[2].markdown("<div style='text-align:right'><b style='font-size:11px;'>Contacto</b></div>", unsafe_allow_html=True)
            st.markdown("---")

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    # FILA (No se apila gracias al CSS del punto 2)
                    fila = st.columns([1, 0.8, 1.2])
                    
                    with fila[0]:
                        st.markdown(f"<p class='tabla-texto'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<p class='tabla-texto' style='text-align:right'>{val_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver"):
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
    st.error("Error al cargar Excel.")
