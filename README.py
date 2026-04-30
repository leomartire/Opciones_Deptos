import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS GLOBAL (Optimizado para Centrado y Tamaño)
st.markdown("""
    <style>
    /* Centrado y ancho máximo del contenedor */
    .main-container {
        max-width: 350px;
        margin: 0 auto;
    }
    
    /* Forzar que el body no tenga paddings gigantes en móvil */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Estilo para los textos de la tabla */
    .tabla-texto {
        font-size: 11px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }

    /* Botones ultra compactos */
    .stButton>button {
        height: 22px !important;
        padding: 0px 8px !important;
        font-size: 10px !important;
        min-height: 22px !important;
        width: 100% !important;
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
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        # Imagen y Título
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
        
        st.markdown("<h3 style='text-align: center; font-size: 16px;'>Panel de Control</h3>", unsafe_allow_html=True)
        st.markdown("---")

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado Manual (Fijo)
            # Usamos columnas de Streamlit pero muy apretadas
            h = st.columns([1, 0.8, 1.2], gap="small")
            h[0].write("**Unidad**")
            h[1].write("**Acción**")
            h[2].write("**Contacto**")

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    # FILA DE DATOS
                    # Usamos columnas de Streamlit. Para evitar que se rompan en móvil, 
                    # el secreto es que el contenido sea muy corto.
                    fila = st.columns([1, 0.8, 1.2], gap="small")
                    
                    with fila[0]:
                        st.markdown(f"<p class='tabla-texto'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        # Cortamos el texto si es muy largo para que no rompa la fila
                        contacto_breve = (val_contacto[:12] + '..') if len(val_contacto) > 14 else val_contacto
                        st.markdown(f"<p class='tabla-texto' style='text-align:right'>{contacto_breve}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        # (Tu código de detalle se mantiene igual)
        opcion = st.session_state.opcion_actual
        if st.button("← Volver"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            with col_t: st.table(df_ficha)
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img): st.image(ruta_img, use_container_width=True)
else:
    st.error("Archivo no encontrado.")
