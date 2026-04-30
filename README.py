import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS (Sin filtros raros, directo del Excel)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos como texto para que respete tus puntos de miles manuales
            return pd.read_excel(archivo, sheet_name=None, dtype=str)
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
            
            # Mostramos la hoja HOME tal cual, eliminando solo si aparece la columna Unnamed de índice
            df_home = diccionario_hojas["HOME"]
            if "Unnamed: 0" in df_home.columns:
                df_home = df_home.drop(columns=["Unnamed: 0"])
            
            # Mostramos tu tabla de contactos/unidades
            st.table(df_home)
            
            st.markdown("#### Seleccionar Unidad para Detalle:")
            # Botones para navegar a las otras pestañas
            for unidad in nombres_hojas:
                if unidad == "HOME":
                    continue
                if st.button(f"🔍 Ficha: {unidad}", use_container_width=True):
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
            
            # Quitamos la columna molesta si existe
            if "Unnamed: 0" in df_ficha.columns:
                df_ficha = df_ficha.drop(columns=["Unnamed: 0"])
            
            st.dataframe(df_ficha, use_container_width=True, hide_index=True)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se encontró el archivo Excel.")
