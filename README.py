import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection  # <--- Nueva librería
    
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
@st.cache_data(ttl=0)
def cargar_datos():
    try:
        # La conexión 'conn' debe estar definida arriba de esta función
        # conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Lee todas las pestañas del Google Sheet definido en Secrets
        return conn.read()
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None
        
diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
    # --- CONTENIDO DINÁMICO ---
    
    # Definimos la opción actual. Por defecto empezamos en HOME si existe.
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        
        # --- COLUMNAS PARA INVERTIR IMAGEN Y MENÚ ---
        col_img, col_menu = st.columns([0.5, 1.5], gap="large")
        
        with col_img:
            img_home = "images/HOME.png"
            if os.path.exists(img_home):
                st.image(img_home, use_container_width=True)
            else:
                st.warning("Imagen 'HOME.png' no encontrada en la carpeta /images")
        
        with col_menu:
            
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
        # 1. Identificamos la unidad seleccionada
        opcion = st.session_state.opcion_actual if "opcion_actual" in st.session_state else opcion
        
        # 2. Limpiamos la palabra "HOME" del título
        titulo_limpio = opcion.replace("HOME", "").strip()
        
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
            
        # Título achicado y limpio
        st.markdown(f"<h1 style='font-size: 1.6rem !important;'>Análisis: {titulo_limpio}</h1>", unsafe_allow_html=True)
        
        # 3. Determinamos qué hoja del Excel leer
        hoja_actual = "Aviso" if (opcion == "Tagle 2554" and "Aviso" in diccionario_hojas) else opcion
        
        if hoja_actual in diccionario_hojas and hoja_actual != "HOME":
            df_original = diccionario_hojas[hoja_actual]
            
            # 4. Limpieza de datos (Borramos "HOME" de las celdas y quitamos nulos)
            df_clean = df_original.dropna(how='all').dropna(axis=1, how='all')
            df_clean = df_clean.replace("HOME", "") 
            
            col_main, col_gallery = st.columns([1.2, 0.8], gap="large")
            
            with col_main:
                st.subheader("Ficha Técnica")
                
                # 1. Establecer la conexión con Google Sheets
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                try:
                    # 2. Leer los datos en tiempo real (ttl=0 para que no use caché vieja)
                    df_actual = conn.read(worksheet=hoja_actual, ttl=0)
                    
                    if not df_actual.empty:
                        # 3. Limpieza visual (Unnamed y Formateo)
                        df_viz = df_actual.copy()
                        
                        # Limpiar encabezados "Unnamed"
                        nuevos_cols = []
                        for i, col in enumerate(df_viz.columns):
                            if "Unnamed" in str(col):
                                nuevos_cols.append(f" " * (i + 1))
                            else:
                                nuevos_cols.append(col)
                        df_viz.columns = nuevos_cols

                        # 4. TABLA EDITABLE: Aquí es donde puedes escribir
                        df_editado = st.data_editor(
                            df_viz, 
                            use_container_width=True, 
                            hide_index=True,
                            key=f"editor_{hoja_actual}"
                        )
                        
                        # 5. BOTÓN MÁGICO PARA GUARDAR
                        st.write("---")
                        if st.button("💾 Guardar cambios en Google Drive"):
                            # Volvemos a poner los nombres originales a las columnas antes de guardar
                            df_para_guardar = df_editado.copy()
                            df_para_guardar.columns = df_actual.columns
                            
                            # Actualizamos la hoja en la nube
                            conn.update(worksheet=hoja_actual, data=df_para_guardar)
                            st.success("¡Datos guardados correctamente!")
                            st.cache_data.clear() # Forzamos la recarga de datos
                            st.rerun()

                        # Botones de links (permanecen igual)
                        for val in df_actual.values.flatten():
                            txt = str(val).strip()
                            if "http" in txt.lower():
                                start = txt.lower().find("http")
                                url = txt[start:].split()[0].split('\n')[0]
                                st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
                    else:
                        st.warning("La hoja está vacía.")
                        
                except Exception as e:
                    st.error(f"Error de conexión: Asegúrate de que la pestaña '{hoja_actual}' exista en tu Google Sheet.")
