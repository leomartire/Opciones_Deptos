import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

# --- CONFIGURACIÓN DE FUENTE PALATINO LINOTYPE ---
st.markdown("""
    <style>
    /* Importamos fuentes similares de Google por si el sistema no tiene Palatino */
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');

    /* Aplicamos Palatino Linotype como prioridad, Lora como alternativa */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, table {
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif !important;
    }
    
    /* Ajuste extra: Palatino suele verse un poco más chica, subimos levemente el tamaño base */
    p, li, label, table {
        font-size: 1.05rem !important;
    }

    /* Estilo para las tablas y fondo */
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
    except Exception as e:
        return None

diccionario_hojas = cargar_datos()

df = diccionario_hojas[opcion]    
    # Limpieza inicial: quitamos filas y columnas totalmente vacías
    if df is not None:
        df_clean = df.dropna(how='all').dropna(axis=1, how='all')
    else:
        df_clean = pd.DataFrame() # Creamos un dataframe vacío para que no explote

    # --- CUERPO PRINCIPAL ---
    st.title(f"📍 {opcion}")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Ficha Técnica")
        
        # VALIDACIÓN CRÍTICA: ¿Tiene datos el dataframe?
        if not df_clean.empty:
            try:
                # Convertimos todo a texto de forma segura para la tabla
                df_mostrar = df_clean.astype(str)
                # Mostramos usando dataframe que es más estable con el índice
                st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Error al mostrar la tabla: {e}")
            
            st.divider()
            st.write("🔗 **Accesos Directos:**")

            # Búsqueda de links (Botones)
            links_encontrados = []
            for fila in df_clean.values:
                for celda in fila:
                    celda_str = str(celda).strip()
                    if "http" in celda_str.lower():
                        # Extraer link limpio
                        inicio = celda_str.find("http")
                        link_limpio = celda_str[inicio:].split(" ")[0].split("\n")[0]
                        links_encontrados.append(link_limpio)
            
            if links_encontrados:
                # Eliminar duplicados y crear botones
                for url in sorted(list(set(links_encontrados))):
                    st.link_button("🚀 Ver Publicación Original", url, use_container_width=True, type="primary")
            else:
                st.info("No se detectaron links en esta pestaña.")
        else:
            st.warning("La pestaña seleccionada no tiene datos válidos o está vacía.")
            
        with col2:
            st.subheader("Galería")
            # El código busca en la carpeta 'fotos' con extensión .jpg
            ruta_foto = f"images/{opcion}.png"
            
            if os.path.exists(ruta_foto):
                st.image(ruta_foto, caption=f"Propiedad: {opcion}", use_container_width=True)
            else:
                st.info(f"💡 Falta subir la foto: images/{opcion}.png")
