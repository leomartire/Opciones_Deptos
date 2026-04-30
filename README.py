import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CSS PARA CENTRADO Y TABLA (Blindado)
st.markdown("""
    <style>
    /* Centrar el bloque principal en PC */
    @media (min-width: 1024px) {
        .block-container {
            max-width: 400px !important;
            margin: auto !important;
        }
    }
    
    /* Reset de padding para móvil */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Estilo para los botones dentro de la tabla */
    .stButton>button {
        height: 24px !important;
        padding: 0px 10px !important;
        font-size: 11px !important;
        width: 100% !important;
    }

    /* Forzamos que la tabla ocupe todo el ancho disponible */
    .tabla-app {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    .tabla-app td {
        padding: 8px 4px;
        border-bottom: 1px solid #eee;
        vertical-align: middle;
    }
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
        # Imagen pequeña y centrada
        if os.path.exists("images/HOME.png"):
            # Usamos un div para centrar y dimensionar la imagen
            st.markdown("<div style='text-align: center;'><img src='app/static/images/HOME.png' style='width: 120px;'></div>", unsafe_allow_html=True)
            # Si la línea de arriba no carga la imagen por la ruta, usa la nativa:
            # st.image("images/HOME.png", width=120)
        
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Panel de Control</h3>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Renderizamos la tabla fila por fila
            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                # Usamos st.columns pero SIN gap para que no se apilen
                c1, c2, c3 = st.columns([1, 0.8, 1.2])
                
                with c1:
                    st.markdown(f"<p style='margin: 5px 0; font-weight: bold;'>{val_unidad}</p>", unsafe_allow_html=True)
                
                with c2:
                    if st.button("Ver", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                
                with c3:
                    val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                    st.markdown(f"<div style='text-align: right; margin: 5px 0;'>{val_contacto}</div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 2px 0; opacity: 0.2;'>", unsafe_allow_html=True)

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
