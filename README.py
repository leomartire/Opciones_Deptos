import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

# Estilo personalizado
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        return pd.read_excel(archivo, sheet_name=None)
    except Exception as e:
        return None

diccionario_hojas = cargar_datos()

if diccionario_hojas is None:
    st.error("No se pudo encontrar el archivo Opciones_Deptos_LM.xlsx. Revisa el nombre en GitHub.")
else:
    # --- NAVEGACIÓN (SIDEBAR) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
    st.sidebar.title("Inversiones Inmobiliarias")
    
    nombres_hojas = list(diccionario_hojas.keys())
    opcion = st.sidebar.radio("Selecciona una opción:", nombres_hojas)

    # Obtenemos el dataframe de la opción elegida
    df = diccionario_hojas[opcion]
    df = df.dropna(how='all').dropna(axis=1, how='all')

    # --- LÓGICA DE VISUALIZACIÓN ---
    
    if opcion == "HOME":
        # --- DISEÑO PANTALLA PRINCIPAL ---
        st.title("📊 Resumen de Búsqueda")
        st.markdown("### Bienvenido al tablero de control de propiedades")
        
        # Imagen de portada si existe
        ruta_home = "images/HOME.png"
        if os.path.exists(ruta_home):
            st.image(ruta_home, use_container_width=True)
        
        st.write("En este sitio puedes comparar las diferentes opciones que estamos evaluando. "
                 "Usa el menú de la izquierda para ver los detalles, fotos y links de cada propiedad.")

        st.divider()

        # Tabla general
        st.subheader("📋 Lista Comparativa")
        st.dataframe(df, use_container_width=True, hide_index=True)

        
    else:
        # --- DISEÑO PANTALLA DEPARTAMENTO ---
        st.title(f"📍 {opcion}")
        
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Ficha Técnica")
            st.table(df)

            # Detector de Links
            for r_idx, row in df.iterrows():
                for val in row:
                    if isinstance(val, str) and "http" in val:
                        st.link_button(f"🔗 Ver publicación original", val, type="primary")

        with col2:
            st.subheader("Galería")
            # El código busca en la carpeta 'fotos' con extensión .jpg
            ruta_foto = f"images/{opcion}.png"
            
            if os.path.exists(ruta_foto):
                st.image(ruta_foto, caption=f"Propiedad: {opcion}", use_container_width=True)
            else:
                st.info(f"💡 Falta subir la foto: images/{opcion}.png")
