import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Inversiones", layout="wide")

# 2. CSS DE PRECISIÓN (Sin márgenes locos)
st.markdown("""
    <style>
    /* Contenedor principal: estilo App móvil */
    .app-box {
        max-width: 380px;
        margin: 0 auto;
        font-family: sans-serif;
    }
    
    /* Imagen Home controlada */
    .home-img {
        width: 100%;
        max-width: 180px;
        display: block;
        margin: 0 auto 10px auto;
    }

    /* LA TABLA REAL: Flexbox para que NO se apile en el celular */
    .fila-tabla {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    .col-unidad { flex: 2; font-size: 13px; font-weight: bold; }
    .col-btn { flex: 1; text-align: center; }
    .col-contacto { flex: 2; font-size: 12px; text-align: right; color: #666; }

    /* Estilo del botón de Streamlit para que encaje */
    div.stButton > button {
        width: 100% !important;
        height: 28px !important;
        padding: 0 !important;
        font-size: 11px !important;
        border-radius: 4px;
    }

    /* Ocultar el menú de arriba para ganar espacio */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
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

    # INICIO DEL CONTENEDOR APP
    st.markdown('<div class="app-box">', unsafe_allow_html=True)

    if st.session_state.opcion_actual == "HOME":
        # IMAGEN HOME
        if os.path.exists("images/HOME.png"):
            st.image("images/HOME.png", width=180) # Forzamos ancho pequeño centrado
        
        st.markdown("<h4 style='text-align: center; margin: 10px 0;'>Panel de Control</h4>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # ENCABEZADO MANUAL
            st.markdown("""
                <div class="fila-tabla" style="border-bottom: 2px solid #333;">
                    <div class="col-unidad">Unidad</div>
                    <div class="col-btn">Ver</div>
                    <div class="col-contacto">Contacto</div>
                </div>
            """, unsafe_allow_html=True)

            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                # Renderizado mixto: HTML para estructura, st.columns solo para el botón
                # para que el botón de Streamlit siga siendo funcional.
                
                cont_fila = st.container()
                with cont_fila:
                    c1, c2, c3 = st.columns([1, 0.7, 1.2])
                    with c1:
                        st.markdown(f"<div class='col-unidad' style='padding-top:5px;'>{val_unidad}</div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("Ver", key=f"btn_{index}"):
                            st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                            st.rerun()
                    with c3:
                        val_cont = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                        st.markdown(f"<div class='col-contacto' style='padding-top:5px;'>{val_cont}</div>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin:0; opacity:0.1'>", unsafe_allow_html=True)

    else:
        # VISTA DETALLE
        if st.button("← Volver"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        opcion = st.session_state.opcion_actual
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            st.table(diccionario_hojas[opcion].dropna(how='all'))
            if os.path.exists(f"images/{opcion}.png"):
                st.image(f"images/{opcion}.png", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True) # CIERRE APP-BOX
else:
    st.error("No se encontró el Excel.")
