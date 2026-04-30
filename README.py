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
        .main-container { max-width: 300px; margin: auto; }
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
            
            # ... (Código de imagen y título) ...

            if "HOME" in diccionario_hojas:
                # Encabezados con los nuevos pesos
                c_head = st.columns([1.1, 0.7, 1.2], gap="small") # <--- Pesos más parejos
                c_head[0].markdown("<b>Unidad</b>", unsafe_allow_html=True)
                c_head[1].markdown("<center><b>Acción</b></center>", unsafe_allow_html=True)
                c_head[2].markdown("<div style='text-align:right'><b>Contacto</b></div>", unsafe_allow_html=True)
                
                st.markdown("---")

                for index, row in df_home.iterrows():
                    # ... (Lógica de filtrado) ...

                    # FILA CON LOS MISMOS PESOS [1.1, 0.7, 1.2]
                    fila = st.columns([1.1, 0.7, 1.2], gap="small")
                    
                    with fila[0]:
                        st.markdown(f"<b>{val_unidad}</b>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales[val_unidad.upper()]
                            st.rerun()
                            
                    with fila[2]:
                        val_contacto = str(row.iloc[2]).strip() if len(row) > 2 else "-"
                        st.markdown(f"<div style='text-align:right'>{val_contacto}</div>", unsafe_allow_html=True)
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
