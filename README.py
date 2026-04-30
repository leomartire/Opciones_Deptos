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

# 3. CARGA DE DATOS (Preservando todo el contenido)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Cargamos sin encabezado para controlar nosotros las filas
            return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    # Mapeo de pestañas para el ruteo
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

   # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        
        # 1. CENTRADO GLOBAL (Afecta a imagen y tabla)
        # Usamos [1, 2, 1] para que el contenido ocupe el 50% central en PC
        # En móviles, Streamlit adaptará estas proporciones automáticamente
        col_izq, col_central, col_der = st.columns([1, 2, 1])
        
        with col_central:
            # IMAGEN CENTRADA
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
            
            st.markdown("## Panel de Control de Inversiones")
            st.markdown("---")

            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"]
                
                # Encabezados de la tabla (ajustados para ser más compactos)
                c_head = st.columns([1, 0.7, 1.3], gap="small")
                c_head[0].markdown("<p class='texto-aplicacion'><b>Unidad</b></p>", unsafe_allow_html=True)
                c_head[1].markdown("<p class='texto-aplicacion'><b>Acción</b></p>", unsafe_allow_html=True)
                c_head[2].markdown("<p class='texto-aplicacion'><b>Contacto</b></p>", unsafe_allow_html=True)
                st.markdown("---")

                unidades_vistas = set()

                for index, row in df_home.iterrows():
                    val_unidad = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
                    
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    
                    unidades_vistas.add(val_unidad)
                    
                    # FILA DE DATOS DENTRO DEL CONTENEDOR CENTRAL
                    fila = st.columns([1, 0.7, 1.3], gap="small")
                    
                    with fila[0]:
                        st.markdown(f"<p class='texto-aplicacion'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        key_match = val_unidad.upper()
                        if key_match in hojas_reales:
                            if st.button("Ver", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[key_match]
                                st.rerun()
                    
                    with fila[2]:
                        val_contacto = str(row.iloc[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                        st.markdown(f"<p class='texto-aplicacion'>{val_contacto}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Ficha Técnica: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            with col_t:
                # Mostramos la tabla completa (Columna A, B, etc.)
                st.table(df_ficha)
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
else:
    st.error("No se pudo leer el archivo Excel.")
