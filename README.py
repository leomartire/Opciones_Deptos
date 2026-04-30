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
            # Leemos como texto para respetar tus formatos de miles manuales
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            # Limpiamos columna de índice si existe
            for nombre in dict_hojas:
                if "Unnamed: 0" in dict_hojas[nombre].columns:
                    dict_hojas[nombre] = dict_hojas[nombre].drop(columns=["Unnamed: 0"])
            return dict_hojas
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME (Solo Unidad, Detalle y Contacto) ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            st.markdown("### Panel de Control de Unidades")
            
            df_home = diccionario_hojas["HOME"].dropna(how='all')
            
            # Definimos anchos para 3 columnas: [Unidad, Botón Detalle, Contacto]
            anchos = [1.5, 1, 2]
            
            # Encabezados
            cols_h = st.columns(anchos)
            cols_h[0].markdown("**Unidad**")
            cols_h[1].markdown("**Detalle**")
            cols_h[2].markdown("**Contacto**")
            st.markdown("---")

            # Filas
            for index, row in df_home.iterrows():
                cols_f = st.columns(anchos)
                
                # Acceso por posición física para evitar errores de etiquetas
                nombre_unidad = str(row.iloc[0]).strip() # Columna 1 del Excel
                # La columna de contacto suele ser la última o cuarta
                # Ajustamos para tomar la columna de contacto (asumiendo que es la 4ta, índice 3)
                info_contacto = row.iloc[3] if len(row) > 3 else "Ver en ficha"
                
                # Columna 1: Nombre de la Unidad
                cols_f[0].write(f"**{nombre_unidad}**")
                
                # Columna 2: Botón de Detalle
                with cols_f[1]:
                    if nombre_unidad in diccionario_hojas and nombre_unidad != "HOME":
                        if st.button("Ver Ficha", key=f"btn_{index}", use_container_width=True):
                            st.session_state.opcion_actual = nombre_unidad
                            st.rerun()
                
                # Columna 3: Información de Contacto
                cols_f[2].write(info_contacto)
                
                st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE (Ficha Técnica) ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # Usamos st.table para asegurar que el formato de texto y puntos sea exacto
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se pudo cargar el archivo Excel.")
