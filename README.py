import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. INICIALIZAR CONEXIÓN
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
    h2 { font-size: 1.4rem !important; color: #334155 !important; font-weight: 500 !important; }
    
    .stRadio [data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)


# 3. CAPA DE DATOS
@st.cache_data(ttl=0)
def cargar_datos():
    try:
        data = conn.read()
        return data
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN Y RENDERIZADO
# Validamos con 'is not None' para evitar errores de ambigüedad de Pandas
if diccionario_hojas is not None:
    
    # Normalizamos la entrada: siempre queremos un diccionario
    if isinstance(diccionario_hojas, pd.DataFrame):
        diccionario_hojas = {"Hoja1": diccionario_hojas}
    
    nombres_hojas = list(diccionario_hojas.keys())
    
    # Inicializamos el estado de la sesión
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
            else:
                st.warning("Imagen 'HOME.png' no encontrada")
        
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

    # --- VISTA DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        titulo_limpio = opcion.replace("HOME", "").strip()
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        st.markdown(f"<h1 style='font-size: 1.6rem !important;'>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
        
        # Lógica de pestañas específicas
        hoja_actual = "Aviso" if (opcion == "Tagle 2554" and "Aviso" in diccionario_hojas) else opcion
        
        if hoja_actual in diccionario_hojas:
            col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
            
            with col_main:
                st.subheader("Ficha Técnica")
                
                try:
                    # Leemos la pestaña específica directamente
                    df_actual = conn.read(worksheet=hoja_actual.strip(), ttl=0)
                    
                    if df_actual is not None and not df_actual.empty:
                        # Limpieza visual
                        df_viz = df_actual.copy()
                        df_viz.columns = [f" " * (i + 1) if "Unnamed" in str(col) else col for i, col in enumerate(df_viz.columns)]

                        # EDITOR DE DATOS
                        df_editado = st.data_editor(
                            df_viz, 
                            use_container_width=True, 
                            hide_index=True,
                            key=f"editor_{hoja_actual}"
                        )
                        
                        st.write("---")
                        if st.button("💾 Guardar cambios en Google Drive"):
                            df_para_guardar = df_editado.copy()
                            df_para_guardar.columns = df_actual.columns
                            
                            conn.update(worksheet=hoja_actual.strip(), data=df_para_guardar)
                            st.success("¡Datos guardados correctamente!")
                            st.cache_data.clear()
                            st.rerun()

                        # Enlaces automáticos
                        for val in df_actual.values.flatten():
                            txt = str(val).strip()
                            if "http" in txt.lower():
                                start = txt.lower().find("http")
                                url = txt[start:].split()[0].split('\n')[0]
                                st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
                    else:
                        st.warning("La hoja seleccionada no tiene datos.")
                        
                except Exception as e:
                    st.error(f"Error al procesar la pestaña '{hoja_actual}': {e}")

            with col_gallery:
                st.subheader("Galería")
                st.info(f"Mostrando multimedia de {titulo_limpio}")
        else:
            st.error(f"La pestaña '{hoja_actual}' no existe en el documento.")
else:
    st.info("Esperando conexión con la base de datos...")
