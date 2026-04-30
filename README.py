import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            # Limpieza profunda de columnas sin nombre o fantasma
            for nombre in dict_hojas:
                df = dict_hojas[nombre]
                dict_hojas[nombre] = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            return dict_hojas
        return None
    except Exception as e:
        st.error(f"Error técnico en el archivo: {e}")
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Mapeo de hojas reales para evitar errores de case-sensitive o espacios
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("---")
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            st.markdown("### Panel de Control de Unidades")
            
            df_home = diccionario_hojas["HOME"].dropna(how='all')
            
            # Definimos anchos: [Unidad (A), Detalle (B), Contacto (C)]
            anchos = [1.5, 1, 2]
            cols_h = st.columns(anchos)
            cols_h[0].markdown("**Unidad**")
            cols_h[1].markdown("**Detalle**")
            cols_h[2].markdown("**Contacto**")
            st.markdown("---")

            for index, row in df_home.iterrows():
                # Validación de datos: Si la columna A está vacía, saltamos la fila
                if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                    continue
                
                cols_f = st.columns(anchos)
                
                # DATA MAPPING ESTRICTO
                nombre_unidad_raw = str(row.iloc[0]).strip() # Columna A
                # El botón se genera con la lógica de la Columna B
                # La info de contacto se toma de la Columna C (índice 2)
                info_contacto = row.iloc[2] if len(row) > 2 else "-"
                
                # Mostrar Nombre Unidad
                cols_f[0].write(f"**{nombre_unidad_raw}**")
                
                # Mostrar Botón de Navegación
                with cols_f[1]:
                    nombre_norm = nombre_unidad_raw.upper()
                    if nombre_norm in hojas_reales and nombre_norm != "HOME":
                        if st.button("Ver Ficha", key=f"nav_{index}", use_container_width=True):
                            st.session_state.opcion_actual = hojas_reales[nombre_norm]
                            st.rerun()
                    else:
                        cols_f[1].write("---")
                
                # Mostrar Contacto
                cols_f[2].write(info_contacto if pd.notnull(info_contacto) else "-")
                
                st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # st.table es fundamental para que tus puntos de miles se vean exactos
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("Archivo 'Opciones_Deptos_LM.xlsx' no detectado.")
