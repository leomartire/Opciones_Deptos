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
            return pd.read_excel(archivo, sheet_name=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
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
            # Eliminamos la columna de índice si existe
            if "Unnamed: 0" in df_home.columns:
                df_home = df_home.drop(columns=["Unnamed: 0"])
            
            # --- RENDERIZADO DE TABLA CON BOTONES INTEGRADOS ---
            # Creamos el encabezado de la tabla
            cols_header = st.columns([1, 1, 1, 1]) 
            headers = df_home.columns.tolist()
            for i, header in enumerate(headers):
                cols_header[i].markdown(f"**{header}**")
            st.markdown("---")

            # Recorremos las filas para poner los datos y el botón
            for index, row in df_home.iterrows():
                c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
                
                # Suponiendo que tus columnas son: Propiedad, Precio, Contacto, Aviso
                # Ajustá los nombres de las columnas según tu Excel exacto
                nombre_unidad = row[0] # Primera columna (ej: Lafinur)
                
                c1.write(row[0])
                c2.write(row[1])
                c3.write(row[2])
                
                # En la cuarta columna (Aviso), ponemos el botón de detalle
                with c4:
                    if st.button("Ver Ficha", key=f"btn_{nombre_unidad}_{index}", use_container_width=True):
                        st.session_state.opcion_actual = nombre_unidad
                        st.rerun()
                st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion]
            if "Unnamed: 0" in df_ficha.columns:
                df_ficha = df_ficha.drop(columns=["Unnamed: 0"])
            
            st.dataframe(df_ficha, use_container_width=True, hide_index=True)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se encontró el archivo Excel.")
