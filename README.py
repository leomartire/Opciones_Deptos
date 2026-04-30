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
    .stMarkdown p {
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
        font-size: 11px !important;
    }    
    .stButton>button {
        height: 1.5em !important;
        padding: 0px 5px !important;
        font-size: 10px !important;
        min-height: 20px !important;
    }
    hr { 
        margin-top: 2px !important; 
        margin-bottom: 2px !important; 
        opacity: 0.2; 
    }
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
        
        # 1. IMAGEN Y TÍTULO (Centrados)
        col_izq, col_central, col_der = st.columns([1, 4, 1])
        with col_central:
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
            st.markdown("<h2 style='text-align: center;'>Panel de Control de Inversiones</h2>", unsafe_allow_html=True)
            st.markdown("---")

            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"]
                unidades_vistas = set()

                # 2. TABLA EN HTML (Ajuste de anchos y altos)
                # Encabezados: Achicamos fuentes y ajustamos flex para comprimir
                st.markdown("""
                    <div style='display: flex; font-weight: bold; text-align: center; border-bottom: 1px solid #ccc; padding-bottom: 2px; font-size: 10px;'>
                        <div style='flex: 1;'>Unidad</div>
                        <div style='flex: 0.6;'>Detalle</div>
                        <div style='flex: 1.4;'>Contacto</div>
                    </div>
                """, unsafe_allow_html=True)

                for index, row in df_home.iterrows():
                    val_unidad = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
                    
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    
                    unidades_vistas.add(val_unidad)
                    
                    # FILA PERSONALIZADA: Proporciones más apretadas [1, 0.6, 1.4]
                    c1, c2, c3 = st.columns([1, 0.6, 1.4], gap="small")
                    
                    with c1:
                        # Reducimos padding-top para pegar más la fila
                        st.markdown(f"<p style='font-size:10px; margin:0; padding-top:2px;'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with c2:
                        key_match = val_unidad.upper()
                        if key_match in hojas_reales:
                            if st.button("Ver", key=f"btn_{index}"):
                                st.session_state.opcion_actual = hojas_reales[key_match]
                                st.rerun()
                    
                    with c3:
                        val_contacto = str(row.iloc[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                        # Alineamos a la izquierda para que no ocupe ancho innecesario centrando
                        st.markdown(f"<p style='font-size:10px; margin:0; padding-top:2px;'>{val_contacto}</p>", unsafe_allow_html=True)
                    
                    # Separador casi invisible y con margen mínimo para achicar el alto total
                    st.markdown("<hr style='margin: 0.1rem 0; opacity: 0.1;'>", unsafe_allow_html=True)
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
