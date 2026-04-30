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
            # Cargamos todo como texto para respetar tus puntos de miles manuales
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            # Limpieza estándar de columnas de índice que crea pandas
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
    # Creamos una lista de nombres de hojas normalizada (sin espacios) para comparar
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
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
            
            # Obtenemos la hoja HOME y limpiamos filas vacías
            df_home = diccionario_hojas["HOME"].dropna(how='all')
            
            # Definimos anchos fijos: Unidad (A), Botón (B), Contacto (C)
            anchos = [1.5, 1, 2]
            
            # Encabezados manuales para asegurar limpieza visual
            cols_h = st.columns(anchos)
            cols_h[0].markdown("**Unidad**")
            cols_h[1].markdown("**Detalle**")
            cols_h[2].markdown("**Contacto**")
            st.markdown("---")

            # Recorremos las filas con iloc para mapeo físico A, B, C
            for index, row in df_home.iterrows():
                # Evitamos procesar si la fila no tiene al menos la columna A
                if len(row) < 1 or pd.isna(row.iloc[0]):
                    continue
                    
                cols_f = st.columns(anchos)
                
                # DATA MAPPING:
                nombre_unidad_raw = str(row.iloc[0]).strip() # Columna A
                nombre_normalizado = nombre_unidad_raw.upper()
                
                # Columna A: Nombre de Unidad
                cols_f[0].write(f"**{nombre_unidad_raw}**")
                
                # Columna B: El Botón (Gatilla la navegación a la pestaña correspondiente)
                with cols_f[1]:
                    # Verificamos si existe una pestaña que coincida con el nombre de la Columna A
                    if nombre_normalizado in hojas_reales and nombre_normalizado != "HOME":
                        if st.button("Ver Ficha", key=f"btn_{index}", use_container_width=True):
                            st.session_state.opcion_actual = hojas_reales[nombre_normalizado]
                            st.rerun()
                    else:
                        cols_f[1].write("---") # Si no hay pestaña detalle
                
                # Columna C: Contacto
                info_contacto = row.iloc[2] if len(row) > 2 else "-"
                cols_f[2].write(info_contacto)
                
                st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # st.table para que no se pierdan los puntos de miles
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se encontró el archivo Excel o la hoja 'HOME'.")
