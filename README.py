import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS (Leemos todo como texto para respetar tu formato manual de Excel)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Usamos dtype=str para que respete los puntos de miles que pusiste a mano
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

    # --- VISTA HOME (Panel con Contactos integrados desde el Excel) ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            st.markdown("### Panel de Control de Unidades")
            
            # Mostramos la tabla HOME que ya tiene los contactos según tu modificación
            df_home = diccionario_hojas["HOME"]
            st.table(df_home)
            
            st.markdown("#### Acceder al Análisis Detallado:")
            
            # Generamos botones solo para las propiedades (hojas que no son HOME)
            for unidad in nombres_hojas:
                if unidad == "HOME":
                    continue
                
                if st.button(f"🔍 Ver Ficha Técnica: {unidad}", use_container_width=True):
                    st.session_state.opcion_actual = unidad
                    st.rerun()

    # --- VISTA DE DETALLE (Ficha Técnica) ---
    else:
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion]
            # Limpiamos vacíos y mostramos (respetando tu formato de texto del Excel)
            st.dataframe(
                df_ficha.dropna(how='all', axis=0).dropna(how='all', axis=1), 
                use_container_width=True, 
                hide_index=True
            )
            
            # Imagen de la propiedad
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
        else:
            st.error("No se encontró la información detallada.")
else:
    st.error("No se pudo cargar el archivo 'Opciones_Deptos_LM.xlsx'.")
