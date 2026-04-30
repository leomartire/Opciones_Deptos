import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS PERSONALIZADO (Look & Feel moderno)
st.markdown("""
    <style>
    /* Estilo para los botones de la tabla */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #1f77b4;
        transition: all 0.3s ease;
        padding: 0px;
        height: 40px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
    }
    .stButton>button:hover {
        border-color: #1f77b4;
        background-color: #f0f8ff;
        transform: scale(1.05);
    }
    /* Limpieza de líneas divisorias */
    hr {
        margin: 0.5rem 0rem !important;
        opacity: 0.3;
    }
    /* Estilo de los encabezados de la tabla */
    .header-text {
        font-weight: bold;
        color: #4a4a4a;
        font-size: 1.1rem;
    }
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
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        st.markdown("## Panel de Gestión de Activos")
        st.markdown("---")
        
        col_img, col_menu = st.columns([0.6, 1.4], gap="large")
        
        with col_img:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
        
        with col_menu:
            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                # Encabezados con estilo
                c_head = st.columns([1.5, 0.8, 2])
                c_head[0].markdown('<p class="header-text">Unidad</p>', unsafe_allow_html=True)
                c_head[1].markdown('<p class="header-text" style="text-align:center;">Ficha</p>', unsafe_allow_html=True)
                c_head[2].markdown('<p class="header-text">Contacto</p>', unsafe_allow_html=True)
                st.markdown("---")

                for index, row in df_home.iterrows():
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                        continue
                    
                    fila = st.columns([1.5, 0.8, 2])
                    
                    # Columna A: Unidad
                    unidad_nombre = str(row.iloc[0]).strip()
                    fila[0].write(f"**{unidad_nombre}**")
                    
                    # Columna B: Botón Estético (Sin texto, solo Icono)
                    with fila[1]:
                        unidad_key = unidad_nombre.upper()
                        if unidad_key in hojas_reales and unidad_key != "HOME":
                            # Usamos una lupa 🔍 como icono minimalista
                            if st.button("🔍", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[unidad_key]
                                st.rerun()
                        else:
                            fila[1].markdown('<p style="text-align:center; color:grey;">-</p>', unsafe_allow_html=True)
                    
                    # Columna C: Contacto
                    contacto_info = row.iloc[2] if len(row) > 2 else "-"
                    fila[2].write(contacto_info if pd.notnull(contacto_info) else "-")
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis Técnico: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            df_ficha = df_ficha.loc[:, ~df_ficha.columns.str.contains('^Unnamed')]
            
            st.table(df_ficha) # Mantiene el formato de miles manual
            
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.markdown("---")
                st.image(ruta_img, width=600)
else:
    st.error("Error al cargar la base de datos.")
