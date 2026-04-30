import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# --- ESTILOS CSS PROFESIONALES (SISTEMA DE DISEÑO LIMPIO) ---
st.markdown("""
    <style>
    /* Importación de fuente de alta calidad */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, label, table {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1e293b;
    }

    /* Fondo de aplicación sutil */
    .stApp {
        background-color: #fcfcfd;
    }

    /* Títulos con peso visual ejecutivo */
    h1 { 
        font-size: 2.2rem !important; 
        font-weight: 600 !important; 
        color: #0f172a !important; 
        letter-spacing: -0.02em;
    }
    
    h2 { font-size: 1.4rem !important; color: #334155 !important; font-weight: 500 !important; }
    h3 { font-size: 1.1rem !important; color: #64748b !important; text-transform: uppercase; letter-spacing: 0.05em; }

    /* Contenedor de bienvenida (Dashboard Card) */
    .dashboard-hero {
        background: white;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin-bottom: 2rem;
    }

    /* Sidebar - Estética original limpia */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Estilo de tablas (Dataframes) */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }

    /* Botones de acción */
    .stButton button, .stLinkButton a {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CAPA DE DATOS (Mantenemos la lógica de negocio)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        return pd.read_excel(archivo, sheet_name=None)
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. NAVEGACIÓN Y ESTRUCTURA
if diccionario_hojas is not None:
    nombres_hojas = list(diccionario_hojas.keys())
    
    # Sidebar: Navegación simple y profesional
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=40)
        st.markdown("### SISTEMA DE GESTIÓN")
        opcion = st.sidebar.radio("Seleccione Unidad:", nombres_hojas, key="nav_v4")
        st.spacer = st.empty()

    # --- PORTADA (HOME) ---
    if opcion == "HOME":
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        st.title("Inversiones Inmobiliarias")
        
        st.markdown("""
            <div class="dashboard-hero">
                <h2 style="margin-top:0;">Resumen Ejecutivo</h2>
                <p style="font-size: 1.1rem; color: #475569; max-width: 800px;">
                    Plataforma de análisis de activos inmobiliarios para la toma de decisiones financieras. 
                    Acceda a las métricas detalladas y documentación de cada unidad mediante el panel lateral.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Resumen visual minimalista
        col_info, col_img = st.columns([1, 1.2])
        with col_info:
            st.subheader("Estado de la Cartera")
            st.write(f"📂 **Unidades en análisis:** {len(nombres_hojas)-1}")
            st.write("📅 **Última actualización:** Abril 2024")
            st.info("Navegue por el panel izquierdo para ver el detalle de cada activo.")
            
        with col_img:
            if os.path.exists("images/home_portada.png"):
                st.image("images/home_portada.png", use_container_width=True)

    # --- DETALLE DE PROPIEDAD (VISTA TÉCNICA) ---
    else:
        st.title(f"{opcion}")
        
        # Lógica de Datos "Espejo"
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
                # Formato numérico profesional
                df_viz = df_clean.map(lambda x: "{:,.0f}".format(x).replace(",", ".") if isinstance(x, (int, float)) else x)
                st.dataframe(df_viz, use_container_width=True, hide_index=True)
                
                # Enlaces de origen
                st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
                for val in df_clean.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        url = txt[txt.lower().find("http"):].split(' ')[0].split('\n')[0]
                        st.link_button("🌐 Acceder a Publicación Original", url, use_container_width=True)
            else:
                st.error("No se han detectado registros válidos en la hoja de Excel.")

        with col_gallery:
            st.subheader("Documentación Visual")
            img_path = f"images/{foto_id}.png"
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True, caption=f"ID: {foto_id}")
            else:
                st.info("Fotografía técnica no disponible.")

else:
    st.error("Error de Sistema: El archivo de origen (Excel) no es accesible.")
