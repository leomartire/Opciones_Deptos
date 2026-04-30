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
    # Creamos un diccionario de mapeo "Limpio" para evitar errores de espacios
    # Esto soluciona problemas como "LAFINUR 3000 " vs "LAFINUR 3000"
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
                df_home = diccionario_hojas["HOME"].dropna(how='all')
                
                c_head = st.columns([1.5, 1, 2])
                c_head[0].markdown("<p class='texto-aplicacion'><b>Unidad</b></p>", unsafe_allow_html=True)
                c_head[1].markdown("<p class='texto-aplicacion'><b>Detalle</b></p>", unsafe_allow_html=True)
                c_head[2].markdown("<p class='texto-aplicacion'><b>Contacto</b></p>", unsafe_allow_html=True)
                st.markdown("---")

                for index, row in df_home.iterrows():
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "":
                        continue
                    
                    fila = st.columns([1.5, 1, 2])
                    
                    # Unidad
                    unidad_nombre = str(row.iloc[0]).strip()
                    fila[0].markdown(f"<p class='texto-aplicacion'><b>{unidad_nombre}</b></p>", unsafe_allow_html=True)
                    
                    # Botón de Detalle con validación mejorada
                    with fila[1]:
                        # Limpiamos el nombre de la unidad para la búsqueda
                        unidad_key = unidad_nombre.upper().strip()
                        
                        if unidad_key in hojas_reales and unidad_key != "HOME":
                            if st.button("Ver Análisis", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[unidad_key]
                                st.rerun()
                        else:
                            # Si no encuentra la pestaña, muestra un aviso sutil
                            fila[1].markdown("<p style='color:orange; font-size:10px;'>Pestaña no encontrada</p>", unsafe_allow_html=True)
                    
                    # Contacto
                    contacto_info = row.iloc[2] if len(row) > 2 else "-"
                    texto_contacto = contacto_info if pd.notnull(contacto_info) else "-"
                    fila[2].markdown(f"<p class='texto-aplicacion'>{texto_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE (TABLA + IMAGEN AL COSTADO) ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Análisis: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0).dropna(how='all', axis=1)
            df_ficha = df_ficha.loc[:, ~df_ficha.columns.str.contains('^Unnamed')]
            
            # Layout de dos columnas: Tabla y Foto
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            
            with col_t:
                st.table(df_ficha)
            
            with col_f:
                # El nombre del archivo debe ser exacto (ej: LAFINUR 3000.png)
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
                else:
                    st.info("Imagen no disponible")
