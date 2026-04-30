import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS GLOBAL (Fuente 12px y Estética)
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 12px !important;
    }
    .stTable td, .stTable th {
        font-size: 12px !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 2.2em;
        background-color: #f0f2f6;
        font-size: 12px !important;
    }
    hr {
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
        opacity: 0.3;
    }
    .texto-aplicacion {
        font-size: 12px !important;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos todas las hojas como texto para no perder ceros a la izquierda o formatos
            return pd.read_excel(archivo, sheet_name=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Mapeo de pestañas para navegación
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("## Panel de Control de Inversiones")
        st.markdown("---")
        
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            if "HOME" in diccionario_hojas:
                # Eliminamos filas que estén totalmente vacías en el Excel
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                # Encabezados de la tabla
                c_head = st.columns([1.5, 1, 2])
                c_head[0].markdown("<p class='texto-aplicacion'><b>Unidad</b></p>", unsafe_allow_html=True)
                c_head[1].markdown("<p class='texto-aplicacion'><b>Detalle</b></p>", unsafe_allow_html=True)
                c_head[2].markdown("<p class='texto-aplicacion'><b>Contacto</b></p>", unsafe_allow_html=True)
                st.markdown("---")

                # Iteramos sobre las filas del Excel para mostrar los datos
                for index, row in df_home.iterrows():
                    # Verificamos si la primera columna (A) tiene el nombre de la unidad
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                        continue
                    
                    fila = st.columns([1.5, 1, 2])
                    
                    # DATA RESTORE: Columna A (Unidad)
                    unidad_nombre = str(row.iloc[0]).strip()
                    fila[0].markdown(f"<p class='texto-aplicacion'><b>{unidad_nombre}</b></p>", unsafe_allow_html=True)
                    
                    # Columna B (Botón de Navegación)
                    with fila[1]:
                        unidad_key = unidad_nombre.upper()
                        if unidad_key in hojas_reales and unidad_key != "HOME":
                            if st.button("Ver Análisis", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[unidad_key]
                                st.rerun()
                        else:
                            fila[1].write("n/a")
                    
                    # DATA RESTORE: Columna C (Contacto)
                    # Tomamos el valor de la tercera columna (índice 2)
                    contacto_info = row.iloc[2] if len(row) > 2 else "-"
                    texto_contacto = contacto_info if pd.notnull(contacto_info) else "-"
                    fila[2].markdown(f"<p class='texto-aplicacion'>{texto_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
            else:
                st.error("No se encontró la pestaña 'HOME' en el archivo.")

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis: {opcion}")
        
        if opcion in diccionario_hojas:
            # Limpieza de la ficha técnica para visualización
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            df_ficha = df_ficha.loc[:, ~df_ficha.columns.str.contains('^Unnamed')]
            
            # Mostramos la tabla (respeta el tamaño 12px del CSS)
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("No se detectó el archivo Excel en el repositorio.")
