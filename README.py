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

# 2. INICIALIZAR CONEXIÓN A GOOGLE SHEETS
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

# 3. LÓGICA DE NAVEGACIÓN Y CARGA DE NOMBRES
# Obtenemos la lista de hojas para el menú (leemos la primera para obtener metadatos)
try:
    # Definimos las unidades manualmente o podrías obtenerlas dinámicamente si prefieres
    nombres_hojas = ["HOME", "Lafinur 3000", "Tagle 2554"] 
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

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
            
        st.markdown(f"<h1 style='font-size: 1.6rem !important;'>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
        
        # Determinamos la hoja técnica
        hoja_actual = "Aviso" if (opcion == "Tagle 2554") else opcion
        
        col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
        
        with col_main:
            st.subheader("Ficha Técnica")
            
            try:
                # LEER DESDE GOOGLE SHEETS
                df_actual = conn.read(worksheet=hoja_actual.strip(), ttl=0)
                
                if not df_actual.empty:
                    # Limpieza visual de columnas Unnamed
                    df_viz = df_actual.copy()
                    df_viz.columns = [f" " * (i + 1) if "Unnamed" in str(col) else col for i, col in enumerate(df_viz.columns)]

                    # TABLA EDITABLE
                    df_editado = st.data_editor(
                        df_viz, 
                        use_container_width=True, 
                        hide_index=True,
                        key=f"editor_{hoja_actual}"
                    )
                    
                    st.write("---")
                    if st.button("💾 Guardar cambios en Google Drive"):
                        # Restauramos columnas originales para el guardado
                        df_para_guardar = df_editado.copy()
                        df_para_guardar.columns = df_actual.columns
                        
                        conn.update(worksheet=hoja_actual.strip(), data=df_para_guardar)
                        st.success("¡Datos guardados correctamente!")
                        st.cache_data.clear()
                        st.rerun()

                    # Links dinámicos
                    for val in df_actual.values.flatten():
                        txt = str(val).strip()
                        if "http" in txt.lower():
                            url = txt[txt.lower().find("http"):].split()[0]
                            st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
                else:
                    st.warning("La hoja está vacía.")
            except Exception as e:
                st.error(f"Error de conexión con la pestaña '{hoja_actual}'")

        with col_gallery:
            st.subheader("Galería")
            # Aquí puedes mantener tu lógica de imágenes actual
            st.info("Imágenes vinculadas a la unidad.")

except Exception as e:
    st.error(f"No se pudo conectar con Google Sheets: {e}")
