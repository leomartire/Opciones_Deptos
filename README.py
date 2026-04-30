import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Inversiones Inmobiliarias", layout="wide", page_icon="🏠")

# --- ESTILOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, table {
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif !important;
    }
    .main { background-color: #f8f9fa; }
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
    
    # Sidebar
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=60)
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Ir a:", nombres_hojas, key="nav_main")

    # --- PORTADA (HOME) ---
    if opcion == "HOME":
        st.title("📊 Panel de Oportunidades")
        
        col_img, col_txt = st.columns([1, 2])
        with col_img:
            if os.path.exists("images/home_portada.png"):
                st.image("images/home_portada.png", use_container_width=True)
        with col_txt:
            st.markdown("### Bienvenido, Leo.")
            st.write("Seleccioná una propiedad en el menú lateral para ver la ficha técnica completa o usá los accesos directos abajo.")

        st.divider()
        st.subheader("🏢 Unidades en Análisis")
        
        # Filtramos para no mostrar el HOME como tarjeta
        items = [h for h in nombres_hojas if h != "HOME"]
        cols = st.columns(3)
        
        for i, depto in enumerate(items):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**📍 {depto}**")
                    # Buscamos el primer link que aparezca en esa hoja
                    df_t = diccionario_hojas[depto]
                    link = next((str(v) for v in df_t.values.flatten() if "http" in str(v).lower()), None)
                    
                    if link:
                        st.link_button("🌐 Ver Aviso Web", link.strip(), use_container_width=True)
                    else:
                        st.write("Detalles en el menú lateral")

    # --- DETALLE DE PROPIEDAD ---
    else:
        st.title(f"📍 {opcion}")
        
        # Lógica Espejo: Tagle 2554 usa los datos de Aviso
        if opcion == "Tagle 2554" and "Aviso" in diccionario_hojas:
            df_display = diccionario_hojas["Aviso"]
            foto_id = "Aviso"
        else:
            df_display = diccionario_hojas[opcion]
            foto_id = opcion

        df_clean = df_display.dropna(how='all').dropna(axis=1, how='all')
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Ficha Técnica")
            if not df_clean.empty:
                # Formato de números: miles con punto y sin decimales
                df_viz = df_clean.map(lambda x: "{:,.0f}".format(x).replace(",", ".") if isinstance(x, (int, float)) else x)
                st.dataframe(df_viz, use_container_width=True, hide_index=True)
                
                st.divider()
                st.write("🔗 **Links Directos:**")
                for val in df_clean.values.flatten():
                    txt = str(val).strip()
                    if "http" in txt.lower():
                        url = txt[txt.lower().find("http"):].split(' ')[0].split('\n')[0]
                        st.link_button("🚀 Abrir Publicación Original", url, use_container_width=True, type="primary")
            else:
                st.info("Sin datos técnicos disponibles.")

        with col2:
            st.subheader("Galería")
            img_path = f"images/{foto_id}.png"
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.info(f"Falta imagen: {img_path}")

else:
    st.error("No se pudo cargar el archivo Excel. Verificá el nombre 'Opciones_Deptos_LM.xlsx'")
