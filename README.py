import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS GLOBAL (Fuente 12px)
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 12px !important; }
    .stTable td, .stTable th { font-size: 12px !important; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 2.2em;
        background-color: #f0f2f6;
        font-size: 12px !important;
    }
    hr { margin-top: 0.4rem; margin-bottom: 0.4rem; opacity: 0.3; }
    .texto-aplicacion { font-size: 12px !important; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Mapeo de pestañas (ignora espacios y mayúsculas)
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
                # Limpiamos filas vacías del Excel
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                # Encabezados
                c_head = st.columns([1.5, 1, 2])
                c_head[0].markdown("<p class='texto-aplicacion'><b>Unidad</b></p>", unsafe_allow_html=True)
                c_head[1].markdown("<p class='texto-aplicacion'><b>Detalle</b></p>", unsafe_allow_html=True)
                c_head[2].markdown("<p class='texto-aplicacion'><b>Contacto</b></p>", unsafe_allow_html=True)
                st.markdown("---")

                # SET para evitar que la lista se repita dos veces
                unidades_procesadas = set()

                for index, row in df_home.iterrows():
                    val_unidad = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
                    
                    # Filtros: No vacíos, no el título "UNIDAD", y no duplicados
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_procesadas:
                        continue
                    
                    unidades_procesadas.add(val_unidad)
                    fila = st.columns([1.5, 1, 2])
                    
                    # Unidad
                    fila[0].markdown(f"<p class='texto-aplicacion'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    # Botón con validación de pestaña
                    with fila[1]:
                        key_busqueda = val_unidad.upper()
                        if key_busqueda in hojas_reales:
                            if st.button("Ver Análisis", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[key_busqueda]
                                st.rerun()
                        else:
                            fila[1].markdown(f"<p style='color:red; font-size:10px;'>Sin pestaña: {val_unidad}</p>", unsafe_allow_html=True)
                    
                    # Contacto
                    val_contacto = str(row.iloc[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                    fila[2].markdown(f"<p class='texto-aplicacion'>{val_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE (TABLA COMPLETA + IMAGEN) ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis: {opcion}")
        
        if opcion in diccionario_hojas:
            # Traemos la hoja de la unidad sin borrar columnas
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            
            # Limpiamos nombres feos de encabezado (Unnamed) para que se vea prolijo
            df_ficha.columns = ["" if "Unnamed" in str(col) else col for col in df_ficha.columns]
            
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            with col_t:
                # Aquí aparecerán Columna A, B y todas las que tengan datos
                st.table(df_ficha)
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
                else:
                    st.info(f"Imagen pendiente: {opcion}.png")
else:
    st.error("Error: Archivo de datos no encontrado.")
