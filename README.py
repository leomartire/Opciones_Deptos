import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. INICIALIZAR CONEXIÓN (La definimos aquí arriba para que todo el programa la use)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS CSS PROFESIONALES ---
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

# 3. CAPA DE DATOS (REPARADA: Ya no busca el .xlsx)
@st.cache_data(ttl=0)
def cargar_datos():
    try:
        # Leemos el archivo de Google directamente
        return conn.read()
    except Exception as e:
        st.error(f"No se pudo conectar con Google Sheets: {e}")
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas is not None:
    # Si Google nos devuelve una sola hoja, la convertimos en lista para que el menú no falle
    if isinstance(diccionario_hojas, pd.DataFrame):
        nombres_hojas = ["HOME"] # O el nombre de tu hoja principal
    else:
        nombres_hojas = list(diccionario_hojas.keys())
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
        
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
        # --- VISTA DE DETALLE (FICHA TÉCNICA) ---
        opcion = st.session_state.opcion_actual
        titulo_limpio = opcion.replace("HOME", "").strip()
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.markdown(f"<h1 style='font-size: 1.6rem !important;'>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
        
        # Determinamos la hoja a leer
        hoja_actual = "Aviso" if (opcion == "Tagle 2554") else opcion
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            st.subheader("Ficha Técnica")
            try:
                # LEER FICHA EN TIEMPO REAL
                df_actual = conn.read(worksheet=hoja_actual.strip(), ttl=0)
                
                if df_actual is not None and not df_actual.empty:
                    df_viz = df_actual.copy()
                    
                    # TABLA EDITABLE
                    df_editado = st.data_editor(
                        df_viz, 
                        use_container_width=True, 
                        hide_index=True,
                        key=f"editor_{hoja_actual}"
                    )
                    
                    if st.button("💾 Guardar cambios en Google Drive"):
                        conn.update(worksheet=hoja_actual.strip(), data=df_editado)
                        st.success("¡Guardado!")
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.warning(f"No hay datos en la pestaña '{hoja_actual}'")
            except Exception as e:
                st.error(f"Error al cargar la ficha: Asegúrate que la pestaña se llame exactamente '{hoja_actual}'")
else:
    st.warning("No se encontraron datos. Revisa la configuración de Google Sheets.")
