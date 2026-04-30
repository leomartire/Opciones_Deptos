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

# 2. INICIALIZAR CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)

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

# 3. CAPA DE DATOS (CORREGIDA PARA RECUPERAR EL MENÚ)
@st.cache_data(ttl=0)
def cargar_todas_las_hojas():
    try:
        # Forzamos a que lea todas las pestañas del Google Sheet
        # Usamos un truco de pandas para obtener los nombres de las hojas
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        all_sheets = pd.read_excel(url, sheet_name=None, engine='openpyxl')
        return all_sheets
    except Exception:
        try:
            # Si falla lo anterior, intentamos la conexión directa de Streamlit
            return conn.read()
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            return None

diccionario_hojas = cargar_todas_las_hojas()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas is not None:
    # Si es un diccionario, sacamos los nombres de las pestañas
    if isinstance(diccionario_hojas, dict):
        nombres_hojas = list(diccionario_hojas.keys())
    else:
        # Si solo trajo una tabla, el menú solo tendrá esa tabla
        nombres_hojas = ["HOME"]

    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME (MENÚ PRINCIPAL) ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
        
        with col_menu:
            st.subheader("Unidades Disponibles")
            seleccion = st.radio(
                "Seleccione una propiedad para ver el detalle:", 
                nombres_hojas, 
                index=nombres_hojas.index("HOME") if "HOME" in nombres_hojas else 0
            )
            
            if seleccion != "HOME":
                if st.button(f"Abrir Ficha de {seleccion}", use_container_width=True):
                    st.session_state.opcion_actual = seleccion
                    st.rerun()

    # --- VISTA DETALLE (LA FICHA TÉCNICA) ---
    else:
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Menú Principal"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.markdown(f"<h1>Análisis de Unidad: {opcion}</h1>", unsafe_allow_html=True)
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            try:
                # Leemos la pestaña específica de Google Sheets
                df_ficha = conn.read(worksheet=opcion.strip(), ttl=0)
                
                if df_ficha is not None and not df_ficha.empty:
                    # Mostramos la tabla para que puedas editarla
                    df_editado = st.data_editor(
                        df_ficha, 
                        use_container_width=True, 
                        hide_index=True,
                        key=f"editor_{opcion}"
                    )
                    
                    if st.button("💾 Guardar Cambios en la Nube"):
                        conn.update(worksheet=opcion.strip(), data=df_editado)
                        st.success("¡Cambios guardados exitosamente!")
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.warning("No se encontraron datos en esta pestaña.")
            except Exception as e:
                st.error(f"No se pudo cargar la pestaña '{opcion}'. Verifica el nombre en Google Sheets.")

else:
    st.error("No se pudo cargar el archivo. Verifica que la URL en 'Secrets' sea correcta.")
