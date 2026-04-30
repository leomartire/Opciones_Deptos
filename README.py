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
    h1 { font-size: 2.2rem !important; font-weight: 600 !important; color: #0f172a !important; }
    h2 { font-size: 1.4rem !important; color: #334155 !important; font-weight: 500 !important; }
    
    /* Contenedor para el radio button lateral derecho */
    .stRadio [data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
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
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    # Sidebar reducido para otros controles si fuera necesario
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=40)
        st.markdown("### PANEL DE CONTROL")
        st.info("Seleccione una unidad en el menú principal para analizar detalles.")

    # --- CONTENIDO DINÁMICO ---
    
    # Definimos la opción actual. Por defecto empezamos en HOME si existe.
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.title("Inversiones Inmobiliarias")
        st.markdown("---")
        
        # --- COLUMNAS PARA INVERTIR IMAGEN Y MENÚ ---
        col_img, col_menu = st.columns([1.5, 0.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
            else:
                st.warning("Imagen 'HOME.png' no encontrada en la carpeta /images")
        
        with col_menu:
            st.markdown("### Oportunidades")
            # El radio button que controla la navegación
            seleccion = st.radio(
                "Seleccione Unidad:", 
                nombres_hojas, 
                index=nombres_hojas.index("HOME") if "HOME" in nombres_hojas else 0
            )
            
            # Botón para confirmar ir al detalle si no es HOME
            if seleccion != "HOME":
                if st.button(f"Ver Detalle de {seleccion}", use_container_width=True):
                    st.session_state.opcion_actual = seleccion
                    st.rerun()

    else:
        # --- VISTA DE DETALLE DE PROPIEDAD ---
        opcion = st.session_state.opcion_actual
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.title(f"Análisis: {opcion}")
        
        # Lógica de datos espejo
        if opcion == "Tagle 2554" and "Aviso" in diccionario_hojas:
            df_display = diccionario_hojas["Aviso"]
            foto_id = "Aviso"
        else:
            df_display = diccionario_hojas[opcion]
            foto_id = opcion

        df_clean = df_display.dropna(how='all').dropna(axis=1, how='all')
        
        c1, c2 = st.columns([1.2, 0.8], gap="large")
        
        with c1:
            st.subheader("Ficha Técnica")
            if not df_clean.empty:
                df_viz = df_clean.map(lambda x: "{:,.0f}".format(x).replace(",", ".")
