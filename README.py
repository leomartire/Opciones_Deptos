import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos como texto para mantener tus puntos de miles manuales
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            
            # Limpiamos cada hoja de las columnas "Unnamed"
            for nombre in dict_hojas:
                df = dict_hojas[nombre]
                # Filtramos para quedarnos solo con columnas que NO empiecen con "Unnamed"
                dict_hojas[nombre] = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            return dict_hojas
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            st.markdown("### Panel de Control de Unidades")
            
            df_home = diccionario_hojas["HOME"]
            # Limpiamos filas vacías que puedan haber quedado en el Excel
            df_home = df_home.dropna(how='all')
            
            st.table(df_home)
            
            st.markdown("#### Acceder al Análisis Detallado:")
            for unidad in nombres_hojas:
                if unidad == "HOME":
                    continue
                if st.button(f"🔍 Ver Ficha Técnica: {unidad}", use_container_width=True):
                    st.session_state.opcion_actual = unidad
                    st.rerun()

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion]
            # Limpiamos filas y columnas totalmente vacías
            df_display = df_ficha.dropna(how='all', axis=0).dropna(how='all', axis=1)
            
            st.dataframe(
                df_display, 
                use_container_width=True, 
                hide_index=True
            )
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se pudo cargar el archivo 'Opciones_Deptos_LM.xlsx'.")
