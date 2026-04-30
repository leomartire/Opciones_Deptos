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
    h1 { font-size: 1.6rem !important; font-weight: 600 !important; color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CAPA DE DATOS: CARGA DINÁMICA DE PESTAÑAS
@st.cache_data(ttl=300)
def obtener_todas_las_unidades():
    try:
        # Intentamos obtener los nombres de las hojas directamente de la conexión
        # Si conn.read() devuelve un dict, sacamos las keys.
        res = conn.read(ttl=0)
        if isinstance(res, dict):
            return list(res.keys())
        # Si no devuelve un dict, es que solo lee una hoja. 
        # Forzamos una lista basada en lo que sabemos que existe en tu Drive
        return ["HOME", "Lafinur 3000", "Tagle 2554", "Acoyte 450", "Pueyrredon 1100"] 
    except Exception:
        return ["HOME", "Lafinur 3000", "Tagle 2554"]

nombres_hojas = obtener_todas_las_unidades()

# 4. LÓGICA DE NAVEGACIÓN
if "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# Sidebar para asegurar que siempre puedes navegar
with st.sidebar:
    st.title("Menú de Unidades")
    seleccion_sidebar = st.selectbox("Ir a:", nombres_hojas, index=nombres_hojas.index(st.session_state.opcion_actual) if st.session_state.opcion_actual in nombres_hojas else 0)
    if seleccion_sidebar != st.session_state.opcion_actual:
        st.session_state.opcion_actual = seleccion_sidebar
        st.rerun()

if st.session_state.opcion_actual == "HOME":
    st.markdown("---")
    col_img, col_menu = st.columns([0.6, 1.4], gap="large")
    
    with col_img:
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
    
    with col_menu:
        st.write("### Bienvenido al Sistema de Gestión")
        st.write("Selecciona una propiedad desde el menú lateral o utiliza los accesos directos.")
        # Botones rápidos para las unidades principales
        for h in [n for n in nombres_hojas if n != "HOME"]:
            if st.button(f"📂 Analizar {h}", key=f"btn_{h}", use_container_width=True):
                st.session_state.opcion_actual = h
                st.rerun()

else:
    # --- VISTA DE DETALLE ---
    opcion = st.session_state.opcion_actual
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
            
    st.markdown(f"<h1>Análisis de Unidad: {opcion}</h1>", unsafe_allow_html=True)
    
    col_main, col_gallery = st.columns([1.3, 0.7], gap="large")
    
    with col_main:
        st.subheader("Ficha Técnica Interactiva")
        try:
            # LEER HOJA ESPECÍFICA DE GOOGLE SHEETS
            df_actual = conn.read(worksheet=opcion.strip(), ttl=0)
            
            if not df_actual.empty:
                # Limpiar datos nulos para la vista
                df_viz = df_actual.dropna(how='all', axis=0).dropna(how='all', axis=1)
                
                # EDITOR DE DATOS (LECTURA Y ESCRITURA)
                df_editado = st.data_editor(
                    df_viz, 
                    use_container_width=True, 
                    hide_index=True,
                    key=f"editor_{opcion}"
                )
                
                if st.button("💾 Guardar cambios en la Nube"):
                    conn.update(worksheet=opcion.strip(), data=df_editado)
                    st.success(f"¡Cambios guardados en la pestaña {opcion}!")
                    st.cache_data.clear()
                    st.rerun()
                
                # Links automáticos si existen en la tabla
                for val in df_actual.values.flatten():
                    if "http" in str(val).lower():
                        url = str(val)[str(val).lower().find("http"):].split()[0]
                        st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
            else:
                st.warning("No hay datos en esta pestaña.")
        except Exception as e:
            st.error(f"Error al conectar con la pestaña '{opcion}'.")
            st.info("Asegúrate de que el nombre de la pestaña en Google Sheets coincida exactamente.")

    with col_gallery:
        st.subheader("Galería de Fotos")
        st.info(f"Cargando multimedia para {opcion}...")
