import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', sans-serif !important;
        color: #1e293b;
    }

    .stApp { background-color: #fcfcfd; }

    h1 { 
        font-size: 2.2rem !important; 
        font-weight: 600 !important; 
        color: #0f172a !important; 
        letter-spacing: -0.02em;
    }
    
    h2 { font-size: 1.4rem !important; color: #334155 !important; font-weight: 500 !important; }
    h3 { font-size: 1.1rem !important; color: #64748b !important; text-transform: uppercase; letter-spacing: 0.05em; }

    /* Estilo de tablas */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CAPA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None)
        return None
    except Exception as e:
        st.error(f"Error al leer Excel: {e}")
        return None

diccionario_hojas = cargar_datos()

# 3. NAVEGACIÓN Y LÓGICA PRINCIPAL
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=50)
        st.markdown("### SISTEMA DE GESTIÓN")
        opcion = st.radio("Seleccione Unidad:", nombres_hojas)

    # --- LÓGICA DE RENDERIZADO ---
    
    if opcion == "HOME":
        img_home = "images/HOME.png"
        if os.path.exists(img_home):
            st.image(img_home, use_container_width=True)
        else:
            st.info("Bienvenido. Seleccione una unidad en el menú lateral para ver el análisis detallado.")

    else:
        # VISTA DE DETALLE DE PROPIEDAD
        st.title(f"Unidad: {opcion}")
        
        # Lógica de Datos "Espejo" para casos especiales
        if opcion == "Tagle 2554" and "Aviso" in diccionario_hojas:
            df_display = diccionario_hojas["Aviso"]
            foto_id = "Aviso"
        else:
            df_display = diccionario_hojas[opcion]
            foto_id = opcion

        df_clean = df_display.dropna(how='all').dropna(axis=1, how='all')
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            st.subheader("Análisis de la Unidad")
            if not df_clean.empty:
                # Formato numérico para moneda y miles
                df_viz = df_clean.map(lambda x: "{:,.0f}".format(x).replace(",", ".") if isinstance(x, (int, float)) else x)
                st.dataframe(df_viz, use_container_width=True, hide_index=True)
                
                # Extracción de links
                for val in df_clean.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        # Intenta limpiar el string para obtener solo la URL
                        url = txt[txt.lower().find("http"):].split(' ')[0].split('\n')[0]
                        st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
            else:
                st.warning("No hay datos disponibles para esta unidad.")

        with col_gallery:
            st.subheader("Documentación Visual")
            img_path = f"images/{foto_id}.png"
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True, caption=f"ID Ref: {foto_id}")
            else:
                st.info("Fotografía técnica o plano no disponible.")
else:
    st.error("Archivo 'Opciones_Deptos_LM.xlsx' no encontrado. Por favor, asegúrese de que el archivo esté en la raíz del proyecto.")
