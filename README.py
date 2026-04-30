import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS (Mantenemos el formato de texto para tus miles manuales)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos todo como string para que no se rompa el formato del Excel
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            # Limpieza rápida de la columna de índice fantasma
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
            
            df_home = diccionario_hojas["HOME"].dropna(how='all')
            num_cols = len(df_home.columns)
            
            # Definimos anchos de columna proporcionales
            anchos = [1.5] + [1] * (num_cols - 1)
            
            # Encabezados
            cols_h = st.columns(anchos)
            for i, col_name in enumerate(df_home.columns):
                cols_h[i].markdown(f"**{col_name}**")
            st.markdown("---")

            # Filas con el botón integrado en la última columna
            for index, row in df_home.iterrows():
                cols_f = st.columns(anchos)
                
                # Nombre de la unidad para la navegación (siempre primera columna)
                unidad_destino = str(row.iloc[0]).strip()
                
                for i in range(num_cols):
                    if i == num_cols - 1: # Si es la última columna (Aviso/Link)
                        with cols_f[i]:
                            # Solo creamos el botón si la unidad existe como pestaña
                            if unidad_destino in diccionario_hojas and unidad_destino != "HOME":
                                if st.button("Ver Ficha", key=f"btn_{index}"):
                                    st.session_state.opcion_actual = unidad_destino
                                    st.rerun()
                            else:
                                cols_f[i].write("-")
                    else:
                        cols_f[i].write(row.iloc[i])
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
            
            # Usamos st.table para que respete al 100% el texto de tus celdas
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se encontró el archivo Excel o el formato es incorrecto.")
