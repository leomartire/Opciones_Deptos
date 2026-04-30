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
            # Leemos como texto para respetar tus puntos de miles manuales
            dict_hojas = pd.read_excel(archivo, sheet_name=None, dtype=str)
            
            # Limpieza de columnas fantasma en cada hoja
            for nombre in dict_hojas:
                df = dict_hojas[nombre]
                # Eliminamos la columna de índice si existe
                if "Unnamed: 0" in df.columns:
                    df = df.drop(columns=["Unnamed: 0"])
                # Eliminamos cualquier columna que sea totalmente vacía
                dict_hojas[nombre] = df.dropna(how='all', axis=1)
            return dict_hojas
        return None
    except Exception as e:
        st.error(f"Error al cargar Excel: {e}")
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Normalización para búsqueda de pestañas
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
            
            # Validamos que exista la hoja HOME
            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                # Columnas visuales: [A: Unidad | B: Botón | C: Contacto]
                anchos = [1.5, 1, 2]
                cols_h = st.columns(anchos)
                cols_h[0].markdown("**Unidad**")
                cols_h[1].markdown("**Detalle**")
                cols_h[2].markdown("**Contacto**")
                st.markdown("---")

                # Recorremos filas con iloc (mapeo físico estricto)
                for index, row in df_home.iterrows():
                    # Si la primera celda está vacía, saltamos
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                        continue
                        
                    cols_f = st.columns(anchos)
                    
                    # DATA MAPPING
                    nombre_unidad_raw = str(row.iloc[0]).strip() # Columna A
                    nombre_norm = nombre_unidad_raw.upper()
                    
                    # 1. Columna Unidad
                    cols_f[0].write(f"**{nombre_unidad_raw}**")
                    
                    # 2. Columna Botón (Basado en la posición B)
                    with cols_f[1]:
                        if nombre_norm in hojas_reales and nombre_norm != "HOME":
                            if st.button("Ver Ficha", key=f"btn_{index}", use_container_width=True):
                                st.session_state.opcion_actual = hojas_reales[nombre_norm]
                                st.rerun()
                        else:
                            cols_f[1].write("---")
                    
                    # 3. Columna Contacto (Columna C)
                    info_contacto = row.iloc[2] if len(row) > 2 else "-"
                    cols_f[2].write(info_contacto if pd.notnull(info_contacto) else "-")
                    
                    st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
            else:
                st.error("No se encontró la pestaña 'HOME' en el Excel.")

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Inicio"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            # st.table es vital para respetar tus puntos de miles manuales
            st.table(df_ficha)
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=500)
else:
    st.error("Archivo 'Opciones_Deptos_LM.xlsx' no detectado o vacío.")
