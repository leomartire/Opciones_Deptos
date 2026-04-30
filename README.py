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
                if not df_clean.empty:
                    # Formateo numérico y reemplazo de "None" por vacío
                    df_viz = df_clean.map(
                        lambda x: "{:,.0f}".format(x).replace(",", ".") 
                        if isinstance(x, (int, float)) and not pd.isna(x) 
                        else ("" if pd.isna(x) else x)
                    )
                    
                    st.dataframe(df_viz, use_container_width=True, hide_index=True)
                    
                    # Generación de botones para links
                    for val in df_clean.values.flatten():
                        txt = str(val).strip()
                        if "http" in txt.lower():
                            url = txt[txt.lower().find("http"):].split()[0]
                            st.link_button("🌐 Ver Publicación Original", url, use_container_width=True)
                else:
                    st.warning("No se encontraron registros técnicos en esta hoja.")

            with col_gallery:
                st.subheader("Documentación")
                # Buscamos imagen por nombre de hoja o unidad
                img_path = f"images/{hoja_actual}.png"
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.info("Fotografía técnica no disponible.")
        else:
            if hoja_actual != "HOME":
                st.error(f"Error: No existe la hoja '{hoja_actual}' en el archivo Excel.")

else:
    st.error("Error de Sistema: El archivo 'Opciones_Deptos_LM.xlsx' no es accesible.")
