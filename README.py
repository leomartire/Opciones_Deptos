import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', sans-serif !important;
        color: #1e293b;
    }
    .stApp { background-color: #fcfcfd; }
    h1 { font-size: 2.2rem !important; font-weight: 600 !important; color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS (Excel Local)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            # Visualización de la imagen principal
            ruta_home = "images/HOME.png"
            if os.path.exists(ruta_home):
                st.image(ruta_home, use_container_width=True)
        
        with col_menu:
            seleccion = st.radio(
                "Seleccione Unidad:", 
                nombres_hojas, 
                index=nombres_hojas.index("HOME") if "HOME" in nombres_hojas else 0
            )
            
            if seleccion != "HOME":
                if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                    st.session_state.opcion_actual = seleccion
                    st.rerun()

    else:
        # --- VISTA DE DETALLE CON IMÁGENES ---
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.markdown(f"<h1>Análisis: {opcion}</h1>", unsafe_allow_html=True)
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            df = diccionario_hojas[opcion]
            df_clean = df.dropna(how='all').dropna(axis=1, how='all')
            st.subheader("Ficha Técnica")
           if vista == "FICHA":
            st.subheader(f"Análisis Técnico: {opcion}")
            
            # 1. Recuperamos la hoja del diccionario
            df = diccionario_hojas[opcion]
            
            # 2. Limpiamos filas y columnas vacías
            df_clean = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

            # --- 3. CONFIGURACIÓN DE FORMATO (AQUÍ VA EL CAMBIO) ---
            # Identificamos las columnas que son números (Precios, m2, etc.)
            cols_numericas = df_clean.select_dtypes(include=['number']).columns
            
            st.dataframe(
                df_clean, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    col: st.column_config.NumberColumn(
                        format="%d",  # %d es para números enteros con separador de miles
                    ) for col in cols_numericas
                }
            )
            # -------------------------------------------------------
            
            # Galería debajo de la ficha
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)

        with col_gallery:
            st.subheader("Galería")
            # El código busca una imagen que se llame igual que la pestaña (ej: Lafinur 3000.png)
            ruta_imagen = f"images/{opcion}.png"
            ruta_jpg = f"images/{opcion}.jpg"
            
            if os.path.exists(ruta_imagen):
                st.image(ruta_imagen, caption=opcion, use_container_width=True)
            elif os.path.exists(ruta_jpg):
                st.image(ruta_jpg, caption=opcion, use_container_width=True)
            else:
                st.info(f"No hay imagen disponible para {opcion} en la carpeta 'images/'")

else:
    st.error("No se encontró el archivo 'Opciones_Deptos_LM.xlsx'.")
