import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Inversiones Inmobiliarias | Panel de Control", layout="wide", page_icon="🏠")

# --- ESTILOS CSS AVANZADOS (ESTILO CORPORATIVO Y CENTRADO DE SIDEBAR) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, table {
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif !important;
    }
    
    /* Estilo para el contenedor principal */
    .main { background-color: #f4f7f9; }
    
    /* Títulos Ejecutivos */
    h1 { font-size: 1.8rem !important; color: #1e3a8a !important; font-weight: 700 !important; margin-bottom: 10px !important; }
    h3 { font-size: 1.1rem !important; color: #475569 !important; font-weight: 600 !important; }

    /* Ajuste de tablas */
    .stDataFrame { border: 1px solid #e2e8f0; border-radius: 8px; background-color: white; padding: 10px; }
    
    /* Etiquetas de bienvenida */
    .welcome-box {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 25px;
    }

    /* --- CENTRADO DEL MENU LATERAL --- */
    [data-testid="stSidebarNav"] {
        display: flex;
        justify-content: center;
    }
    
    section[data-testid="stSidebar"] > div {
        text-align: center;
    }

    /* Centrar imagen en sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-left: auto;
        margin-right: auto;
    }

    /* Centrar radio buttons y textos en sidebar */
    [data-testid="stSidebar"] .st-expander, [data-testid="stSidebar"] .stRadio > label {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        return pd.read_excel(archivo, sheet_name=None)
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas is not None:
    nombres_hojas = list(diccionario_hojas.keys())
    
    # Sidebar Corporativo (Ahora centrado por CSS)
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=60)
    st.sidebar.markdown("### Navegación")
    opcion = st.sidebar.radio("Ir a:", nombres_hojas, key="nav_main_v3")

    # --- PORTADA (HOME - MINIMALISTA ABSOLUTA) ---
    if opcion == "HOME":
        st.title("📊 Panel de Control Inmobiliario")
        
        st.markdown(f"""
            <div class="welcome-box">
                <span style="color: #64748b; font-size: 0.85rem; text-transform: uppercase; font-weight: bold;">Leonardo Martire | Inversiones</span>
                <p style="margin-top: 10px; color: #1e293b; font-size: 1.1rem; line-height: 1.6;">
                    Bienvenido al centro de monitoreo de oportunidades. <br>
                    Utilice el <b>menú lateral de la izquierda</b> para navegar entre las propiedades y acceder al <b>Detalle de Inversión</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()
        
        # Imagen de fondo sutil
        if os.path.exists("images/home_portada.png"):
            st.image("images/home_portada.png", width=350)
        else:
            st.info("👈 Seleccione una unidad en el menú para comenzar el análisis.")

    # --- DETALLE DE PROPIEDAD ---
    else:
        st.title(f"📍 {opcion}")
        
        # Lógica Espejo para Tagle 2554
        if opcion == "Tagle 2554" and "Aviso" in diccionario_hojas:
            df_display = diccionario_hojas["Aviso"]
            foto_id = "Aviso"
        else:
            df_display = diccionario_hojas[opcion]
            foto_id = opcion

        df_clean = df_display.dropna(how='all').dropna(axis=1, how='all')
        
        c1, c2 = st.columns([1.2, 0.8])
        
        with c1:
            st.subheader("Detalle de Inversión")
            if not df_clean.empty:
                # Formateo de números (miles con punto, 0 decimales)
                df_viz = df_clean.map(lambda x: "{:,.0f}".format(x).replace(",", ".") if isinstance(x, (int, float)) else x)
                st.dataframe(df_viz, use_container_width=True, hide_index=True)
                
                st.divider()
                st.markdown("### 🔗 Links de Referencia")
                for val in df_clean.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        url = txt[txt.lower().find("http"):].split(' ')[0].split('\n')[0]
                        st.link_button(f"🚀 Ver en Portal Inmobiliario", url, use_container_width=True, type="primary")
            else:
                st.info("No hay datos cargados.")

        with c2:
            st.subheader("Galería")
            img_path = f"images/{foto_id}.png"
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning(f"Imagen pendiente: {img_path}")

else:
    st.error("Archivo Excel no detectado.")
