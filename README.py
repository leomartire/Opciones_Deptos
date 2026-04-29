import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN Y CARGA DE DATOS
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

@st.cache_data
def load_data():
    # ACTUALIZACIÓN: Nombre del nuevo archivo
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        # Cargamos todas las pestañas (sheets)
        return pd.read_excel(archivo, sheet_name=None)
    except Exception as e:
        st.error(f"No se encontró el archivo: {archivo}")
        return None

sheets = load_data()

if sheets:
    # 2. NAVEGACIÓN (SIDEBAR)
    st.sidebar.title("🏙️ Índice de Deptos")
    # El selector muestra los nombres de las pestañas del Excel
    selection = st.sidebar.selectbox("Seleccione una propiedad:", list(sheets.keys()))

    # 3. CUERPO PRINCIPAL
    st.title(f"Detalles: {selection}")

    # Obtener el dataframe de la pestaña seleccionada
    df = sheets[selection]

    # Columnas: Datos a la izquierda (col1) e Imagen a la derecha (col2)
    col1, col2 = st.columns([1, 1])

    with col1:
        if not df.empty:
            # Limpieza para no mostrar filas vacías de Excel
            df_clean = df.dropna(how='all').dropna(axis=1, how='all')
            st.table(df_clean)
            
            # LÓGICA DE LINKS: Buscar cualquier URL en las celdas
            for row in df_clean.values:
                for cell in row:
                    if isinstance(cell, str) and "http" in cell:
                        st.link_button("🌐 Ver publicación original", cell)
        else:
            st.info("Esta pestaña está vacía.")

    with col2:
        # LÓGICA DE IMÁGENES: 
        # Busca en la carpeta 'fotos' un archivo que se llame igual a la pestaña + .jpg
        image_path = f"fotos/{selection}.jpg"
        
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Vista de {selection}", use_container_width=True)
        else:
            st.warning(f"No se encontró la imagen: {selection}.jpg")
            st.info("Asegúrese de que el archivo esté en la carpeta 'fotos' con el nombre exacto de la pestaña.")

else:
    st.error("Error al cargar la base de datos. Verifique el archivo Excel en GitHub.")
