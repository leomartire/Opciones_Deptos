import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

# --- CONFIGURACIÓN DE FUENTE PALATINO LINOTYPE ---
st.markdown("""
    <style>
    /* Importamos fuentes similares de Google por si el sistema no tiene Palatino */
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');

    /* Aplicamos Palatino Linotype como prioridad, Lora como alternativa */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, table {
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif !important;
    }
    
    /* Ajuste extra: Palatino suele verse un poco más chica, subimos levemente el tamaño base */
    p, li, label, table {
        font-size: 1.05rem !important;
    }

    /* Estilo para las tablas y fondo */
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
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
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=60)
    st.sidebar.title("Inversiones Inmobiliarias")
    
    nombres_hojas = list(diccionario_hojas.keys())
    opcion = st.sidebar.radio("Selecciona una opción:", nombres_hojas)

    # Obtenemos el dataframe de la opción elegida
    df = diccionario_hojas[opcion]
    df = df.dropna(how='all').dropna(axis=1, how='all')

    # --- LÓGICA DE VISUALIZACIÓN ---
    
    if opcion == "HOME":
        
        # Imagen de portada si existe
        ruta_home = "images/HOME.png"
        if os.path.exists(ruta_home):
            st.image(ruta_home, width=300)
        
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
