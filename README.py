import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS (Ajuste fino para imagen y tabla)
st.markdown("""
    <style>
    /* Centrado para PC */
    @media (min-width: 1024px) {
        .main-app-container {
            max-width: 450px;
            margin: 0 auto;
        }
    }

    /* EVITAR APILAMIENTO SOLO EN LA TABLA */
    /* Usamos un selector más específico para no afectar a la imagen */
    .row-tabla [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Ajuste de imagen para que no se corte */
    [data-testid="stImage"] img {
        max-width: 100%;
        height: auto;
    }

    .stButton>button {
        height: 26px !important;
        padding: 0px !important;
        font-size: 11px !important;
        width: 100% !important;
    }

    .tabla-texto {
        font-size: 11px !important;
        margin: 0 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    hr { margin: 8px 0 !important; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

if diccionario_hojas:
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # Envolvemos todo en un div para el control de ancho en PC
    st.markdown('<div class="main-app-container">', unsafe_allow_html=True)

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # Imagen Home (Sin columnas para que no se corte)
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", use_container_width=True)
        
        st.markdown("<h3 style='text-align: center; font-size: 18px;'>Panel de Control</h3>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Encabezado con clase específica para el CSS
            st.markdown('<div class="row-tabla">', unsafe_allow_html=True)
            h = st.columns([1, 0.8, 1.2])
            h[0].write("**Unidad**")
            h[1].write("**Acción**")
            h[2].markdown("<div style='text-align:right'>**Contacto**</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")

            if df_home is not None:
                for index, row in df_home.iterrows():
                    val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                    if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                        continue
                    unidades_vistas.add(val_unidad)
                    
                    # FILA con clase para evitar el apilamiento
                    st.markdown('<div class="row-tabla">', unsafe_allow_html=True)
                    fila = st.columns([1, 0.8, 1.2])
                    
                    with fila[0]:
                        st.markdown(f"<p class='tabla-texto'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                    
                    with fila[1]:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    
                    with fila[2]:
                        val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<p class='tabla-texto' style='text-align:right'>{val_contacto}</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("<hr>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        if st.button("← Volver"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            st.table(df_ficha)
            ruta_img = f"images/{opcion}.png"
            if os.path.exists(ruta_img):
                st.image(ruta_img, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Cierre de main-app-container
else:
    st.error("Error al cargar Excel.")
