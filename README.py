import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS GLOBAL (Corregido y Unificado)
st.markdown("""
    <style>
    /* Contenedor principal para centrar en PC */
    @media (min-width: 1024px) {
        .main-container {
            max-width: 600px;
            margin: 0 auto;
        }
    }
    
    /* Ajustes de fuente y espaciado general */
    html, body, [class*="st-"] { font-size: 12px !important; }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    .stMarkdown p {
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
    }

    /* Botones compactos */
    .stButton>button {
        height: 20px !important;
        padding: 0px 10px !important;
        font-size: 10px !important;
        min-height: 20px !important;
        line-height: 1 !important;
        width: auto !important;
    }

    /* Estilo para la fila 'Tabla' responsiva */
    .tabla-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    .col-unidad { flex: 1; font-weight: bold; font-size: 11px; }
    .col-boton { flex: 0.5; text-align: center; }
    .col-contacto { flex: 1.5; text-align: right; font-size: 11px; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
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
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        # IMAGEN Y TÍTULO
        if os.path.exists("images/HOME.png"):
            _, col_img_cnt, _ = st.columns([1, 2, 1])
            with col_img_cnt:
                st.image("images/HOME.png", use_container_width=True)
        
        st.markdown("<h2 style='text-align: center; font-size: 18px;'>Panel de Control de Inversiones</h2>", unsafe_allow_html=True)
        st.markdown("---")

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # ENCABEZADO MANUAL (Simulado para que no se rompa)
            st.markdown("""
                <div class='tabla-row' style='border-bottom: 2px solid #ccc;'>
                    <div class='col-unidad'>Unidad</div>
                    <div class='col-boton'>Acción</div>
                    <div class='col-contacto'>Contacto</div>
                </div>
            """, unsafe_allow_html=True)

            for index, row in df_home.iterrows():
                val_unidad = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
                
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                
                unidades_vistas.add(val_unidad)
                
                # CREACIÓN DE LA FILA (Mezcla de HTML para texto y Streamlit para el botón)
                # Esto garantiza que el texto no se mueva, pero el botón funcione
                c1, c2, c3 = st.columns([1, 0.6, 1.4], gap="small")
                
                with c1:
                    st.markdown(f"<p class='col-unidad'>{val_unidad}</p>", unsafe_allow_html=True)
                with c2:
                    key_match = val_unidad.upper()
                    if key_match in hojas_reales:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales[key_match]
                            st.rerun()
                with c3:
                    val_contacto = str(row.iloc[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                    st.markdown(f"<p class='col-contacto'>{val_contacto}</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 0px; opacity: 0.1;'>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

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
                st.table(df_ficha)
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
else:
    st.error("No se pudo leer el archivo Excel.")
