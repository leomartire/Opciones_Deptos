import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS GLOBAL (Fuente 12px)
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 12px !important; }
    .stTable td, .stTable th { font-size: 12px !important; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 2.2em;
        background-color: #f0f2f6;
        font-size: 12px !important;
    }
    hr { margin-top: 0.4rem; margin-bottom: 0.4rem; opacity: 0.3; }
    .texto-aplicacion { font-size: 12px !important; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("## Panel de Control de Inversiones")
        st.markdown("---")
        
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                c_head = st.columns([1.5, 1, 2])
                c_head[0].markdown("<p class='texto-aplicacion'><b>Unidad</b></p>", unsafe_allow_html=True)
                c_head[1].markdown("<p class='texto-aplicacion'><b>Detalle</b></p>", unsafe_allow_html=True)
                c_head[2].markdown("<p class='texto-aplicacion'><b>Contacto</b></p>", unsafe_allow_html=True)
                st.markdown("---")

                unidades_vistas = set()

                for index, row in df_home.iterrows():
                    val_unidad = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
                    
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    
                    unidades_vistas.add(val_unidad)
                    fila = st.columns([1.5, 1, 2])
                    
                    fila[0].markdown(f"<p class='texto-aplicacion'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        unidad_key = val_unidad.upper()
                        if unidad_key in hojas_reales:
                            if st.button("Ver Análisis", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[unidad_key]
                                st.rerun()
                        else:
                            fila[1].markdown(f"<p style='color:red; font-size:10px;'>Pestaña '{val_unidad}' no hallada</p>", unsafe_allow_html=True)
                    
                    val_contacto = str(row.iloc[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                    fila[2].markdown(f"<p class='texto-aplicacion'>{val_contacto}</p>", unsafe_allow_html=True)
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE (CORREGIDA PARA MOSTRAR TODAS LAS COLUMNAS) ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis: {opcion}")
        
        if opcion in diccionario_hojas:
            # Recuperamos la hoja completa sin filtrar columnas por nombre
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            
            # Reemplazamos nombres de columnas "Unnamed" por espacios vacíos para una visualización limpia
            df_ficha.columns = ["" if "Unnamed" in str(col) else col for col in df_ficha.columns]
            
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            with col_t:
                # Ahora st.table mostrará la columna A y la B (y cualquier otra con datos)
                st.table(df_ficha)
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
else:
    st.error("No se encontró el archivo Excel.")
