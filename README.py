import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Inversiones Inmobiliarias", layout="centered")

# 2. CSS PARA CONTROL TOTAL (Estilo App Nativa)
st.markdown("""
    <style>
    /* Limitar el ancho total para que no se agrande nada */
    .block-container {
        max-width: 400px !important;
        padding-top: 1rem !important;
        margin: auto !important;
    }

    /* Logo: Tamaño recuperado y centrado */
    .logo-container {
        text-align: center;
        margin-bottom: 15px;
    }
    .logo-img {
        width: 320px; /* Tamaño más grande para el logo */
        height: auto;
    }

    /* Tabla HTML: Compacta y fija (No se rompe en móvil) */
    .tabla-fija {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
    }
    .tabla-fija th {
        text-align: left;
        font-size: 12px;
        border-bottom: 2px solid #333;
        padding: 8px 4px;
    }
    .tabla-fija td {
        padding: 10px 4px;
        border-bottom: 1px solid #eee;
        font-size: 13px;
        vertical-align: middle;
    }

    /* Ajuste del botón de Streamlit para que entre en la tabla */
    div.stButton > button {
        width: 100% !important;
        height: 28px !important;
        font-size: 11px !important;
        padding: 0 !important;
    }
    
    .contacto-text {
        font-size: 11px;
        color: #555;
        text-align: right;
    }
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

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # LOGO (Grande y centrado)
        if os.path.exists("images/HOME.png"):
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image("images/HOME.png", width=250) # Logo recuperado
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h4 style='text-align: center; margin: 0;'>Panel de Control</h4>", unsafe_allow_html=True)

        if "HOME" in diccionario_hojas:
            df_home = diccionario_hojas["HOME"]
            unidades_vistas = set()

            # Estructura de Tabla Fija
            st.markdown("""
                <table class="tabla-fija">
                    <tr>
                        <th style="width: 35%;">Unidad</th>
                        <th style="width: 25%;">Ver</th>
                        <th style="width: 40%; text-align: right;">Contacto</th>
                    </tr>
                </table>
            """, unsafe_allow_html=True)

            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                    continue
                unidades_vistas.add(val_unidad)
                
                # Fila con Columnas de Streamlit pero ancho controlado
                col1, col2, col3 = st.columns([1, 0.8, 1.2])
                with col1:
                    st.markdown(f"<div style='padding-top:8px; font-weight:bold; font-size:13px;'>{val_unidad}</div>", unsafe_allow_html=True)
                with col2:
                    if st.button("Ver", key=f"btn_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with col3:
                    val_cont = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                    st.markdown(f"<div class='contacto-text' style='padding-top:10px;'>{val_cont}</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:0; opacity:0.1'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        if st.button("← Volver"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
        
        opcion = st.session_state.opcion_actual
        st.subheader(f"Ficha: {opcion}")
        if opcion in diccionario_hojas:
            st.table(diccionario_hojas[opcion].dropna(how='all'))
            if os.path.exists(f"images/{opcion}.png"):
                st.image(f"images/{opcion}.png", use_container_width=True)
else:
    st.error("Error al cargar Excel.")
