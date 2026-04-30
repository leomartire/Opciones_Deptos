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
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            # Limpieza de columnas fantasma en todas las hojas
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

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            st.markdown("### Panel de Control de Unidades")
            
            df_home = diccionario_hojas["HOME"].dropna(how='all')
            
            # --- AJUSTE DE COLUMNAS ---
            # Suponiendo que tu Excel tiene: [Unidad, Precio, Aviso, Contacto]
            # Queremos mostrar solo: [Unidad, Precio, Contacto, BOTÓN]
            
            # Definimos los anchos para las 4 columnas que mostraremos
            anchos = [1.5, 1, 1.5, 1]
            
            # Encabezados personalizados (saltándonos la columna 'Aviso')
            cols_h = st.columns(anchos)
            cols_h[0].markdown("**Unidad**")
            cols_h[1].markdown("**Precio**")
            cols_h[2].markdown("**Contacto**")
            cols_h[3].markdown("**Acción**")
            st.markdown("---")

            # Filas
            for index, row in df_home.iterrows():
                cols_f = st.columns(anchos)
                
                # Tomamos los datos por posición física para evitar errores de nombre
                unidad_destino = str(row.iloc[0]).strip() # Columna 0: Unidad
                precio = row.iloc[1]                     # Columna 1: Precio
                # Nos saltamos la columna 2 (Aviso)
                contacto = row.iloc[3] if len(row) > 3 else "-" # Columna 3: Contacto
                
                cols_f[0].write(unidad_destino)
                cols_f[1].write(precio)
                cols_f[2].write(contacto)
                
                # Botón de navegación
                with cols_f[3]:
                    if unidad_destino in diccionario_hojas and unidad_destino != "HOME":
                        if st.button("Ver Ficha", key=f"btn_{index}"):
                            st.session_state.opcion_actual = unidad_destino
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
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # Mostramos la ficha técnica con st.table para respetar el formato Excel
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se pudo cargar el archivo Excel.")
