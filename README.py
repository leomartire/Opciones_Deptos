import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# Estilo CSS para mejorar la estética de la tabla manual
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 2em;
        background-color: #f0f2f6;
    }
    hr {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos todas las hojas como texto
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            return dict_hojas
        return None
    except Exception as e:
        st.error(f"Error de lectura: {e}")
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Mapeo de pestañas (Case-insensitive)
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
                # Limpiamos la hoja HOME de filas totalmente vacías
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                # Encabezados de la tabla (Columnas A, B y C del Excel)
                c_head = st.columns([1.5, 1, 2])
                c_head[0].subheader("Unidad")
                c_head[1].subheader("Detalle")
                c_head[2].subheader("Contacto")
                st.markdown("---")

                # Renderizado por fila
                for index, row in df_home.iterrows():
                    # Validar que la Columna A tenga datos
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                        continue
                    
                    fila = st.columns([1.5, 1, 2])
                    
                    # Columna A: Unidad
                    unidad_nombre = str(row.iloc[0]).strip()
                    fila[0].write(f"**{unidad_nombre}**")
                    
                    # Columna B: Botón de Detalle
                    with fila[1]:
                        unidad_key = unidad_nombre.upper()
                        if unidad_key in hojas_reales and unidad_key != "HOME":
                            if st.button("Ver Análisis", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[unidad_key]
                                st.rerun()
                        else:
                            fila[1].write("n/a")
                    
                    # Columna C: Contacto
                    contacto_info = row.iloc[2] if len(row) > 2 else "-"
                    fila[2].write(contacto_info if pd.notnull(contacto_info) else "-")
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
            else:
                st.error("No se encontró la pestaña HOME.")

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel Principal"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Ficha Técnica: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # Eliminamos cualquier columna 'Unnamed' que ensucie la visualización
            df_ficha = df_ficha.loc[:, ~df_ficha.columns.str.contains('^Unnamed')]
            
            # st.table para asegurar que los puntos de miles se vean como en el Excel
            st.table(df_ficha)
            
            # Imagen de la propiedad
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=600)

else:
    st.error("Archivo de datos no encontrado.")
