import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

# --- CONFIGURACIÓN DE FUENTE PALATINO LINOTYPE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, table {
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif !important;
    }
    p, li, label, table {
        font-size: 1.05rem !important;
    }
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
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

# 3. LÓGICA PRINCIPAL
if diccionario_hojas is not None:
    # --- NAVEGACIÓN (SIDEBAR) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=60)
    st.sidebar.title("Inversiones")
    
    nombres_hojas = list(diccionario_hojas.keys())
    opcion = st.sidebar.radio("Selecciona una propiedad:", nombres_hojas, key="nav_radio")

    # PROCESAMIENTO
    df = diccionario_hojas[opcion]
    df_clean = df.dropna(how='all').dropna(axis=1, how='all') if df is not None else pd.DataFrame()

    # --- CUERPO DE LA PÁGINA ---
    if opcion == "HOME":
        st.title("📊 Resumen de Búsqueda")
        ruta_home = "images/home_portada.png" 
        if os.path.exists(ruta_home):
            st.image(ruta_home, width=400)
        st.divider()
        st.subheader("📋 Resumen General")
        st.dataframe(df_clean.astype(str), use_container_width=True, hide_index=True)

    else:
        st.title(f"📍 {opcion}")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Ficha Técnica")
            if not df_clean.empty:
                st.dataframe(df_clean.astype(str), use_container_width=True, hide_index=True)
                st.divider()
                st.write("🔗 **Accesos Directos:**")

                # LÓGICA DE BOTONES (Dentro de col1)
                links_encontrados = []
                for col in df_clean.columns:
                    for valor in df_clean[col]:
                        texto_celda = str(valor).strip()
                        if "http" in texto_celda.lower():
                            inicio = texto_celda.lower().find("http")
                            link_final = texto_celda[inicio:].split(' ')[0].split('\n')[0].split(',')[0]
                            if link_final.startswith("http"):
                                links_encontrados.append(link_final)

                if links_encontrados:
                    links_unicos = list(dict.fromkeys(links_encontrados))
                    for url in links_unicos:
                        st.link_button("🌐 Ver en la Web", url, use_container_width=True, type="primary")
                else:
                    st.info("No se detectaron links.")
            else:
                st.warning("Pestaña vacía.")

        with col2:
            st.subheader("Galería")
            ruta_foto = f"images/{opcion}.png"
            if os.path.exists(ruta_foto):
                st.image(ruta_foto, use_container_width=True)
            else:
                st.info(f"Falta imagen: images/{opcion}.png")

else:
    st.error("No se pudo cargar el Excel. Revisa el nombre del archivo.")
