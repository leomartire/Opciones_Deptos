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

# 3. CAPA DE DATOS DINÁMICA (Google Sheets)
@st.cache_data(ttl=300) # Caché de 5 min para no saturar la conexión
def cargar_nombres_pestañas():
    try:
        # Intentamos leer el archivo para extraer los nombres de las hojas
        # En st-gsheets-connection, esto devuelve un dict de DataFrames
        datos = conn.read()
        if isinstance(datos, dict):
            return list(datos.keys())
        return ["HOME"] # Fallback
    except Exception:
        return ["HOME", "Lafinur 3000", "Tagle 2554"] # Fallback manual si falla la API

nombres_hojas = cargar_nombres_pestañas()

# 4. LÓGICA DE NAVEGACIÓN
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
            index=nombres_hojas.index(st.session_state.opcion_actual) if st.session_state.opcion_actual in nombres_hojas else 0
        )
        
        if seleccion != "HOME":
            if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                st.session_state.opcion_actual = seleccion
                st.rerun()

else:
    # --- VISTA DE DETALLE DE PROPIEDAD ---
    opcion = st.session_state.opcion_actual
    titulo_limpio = opcion.replace("HOME", "").strip()
    
    if st.button("← Volver al Inicio"):
        st.session_state.opcion_actual = "HOME"
        st.rerun()
        
    st.markdown(f"<h1>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
    
    # Determinamos qué hoja leer
    hoja_a_cargar = "Aviso" if (opcion == "Tagle 2554") else opcion
    
    col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
    
    with col_main:
        st.subheader("Ficha Técnica")
        
        try:
            # LEER HOJA ESPECÍFICA
            df_actual = conn.read(worksheet=hoja_a_cargar.strip(), ttl=0)
            
            if not df_actual.empty:
                # Limpieza de datos (quitamos nulos)
                df_clean = df_actual.dropna(how='all', axis=0).dropna(how='all', axis=1)
                
                # Editor de datos
                df_editado = st.data_editor(
                    df_clean, 
                    use_container_width=True, 
                    hide_index=True,
                    key=f"editor_{hoja_a_cargar}"
                )
                
                st.write("---")
                if st.button("💾 Guardar cambios en Google Drive"):
                    conn.update(worksheet=hoja_a_cargar.strip(), data=df_editado)
                    st.success("¡Datos guardados!")
                    st.cache_data.clear()
                    st.rerun()

                # Links automáticos
                for val in df_actual.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        start = txt.lower().find("http")
                        url = txt[start:].split()[0].split('\n')[0]
                        st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
            else:
                st.warning("La hoja está vacía.")
        except Exception as e:
            st.error(f"Error al cargar la pestaña '{hoja_a_cargar}'")

    with col_gallery:
        st.subheader("Galería")
        st.info(f"Información de {titulo_limpio}")
