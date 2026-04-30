import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. CARGA DE DATOS (Excel Local)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            return pd.read_excel(archivo, sheet_name=None)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 3. LÓGICA DE NAVEGACIÓN
if diccionario_hojas:
    nombres_hojas = list(diccionario_hojas.keys())
    
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
            for unidad in nombres_hojas:
                if unidad == "HOME" or unidad == "Contacto":
                    continue
                
                c1, c2, c3 = st.columns([1.5, 1, 1])
                with c1:
                    st.markdown(f"<div style='padding-top: 10px;'><strong>🏢 {unidad}</strong></div>", unsafe_allow_html=True)
                with c2:
                    if st.button(f"🔍 Ficha", key=f"det_{unidad}", use_container_width=True):
                        st.session_state.opcion_actual = unidad
                        st.session_state.vista_interna = "FICHA"
                        st.rerun()
                with c3:
                    if st.button(f"📞 Contacto", key=f"cont_{unidad}", use_container_width=True):
                        st.session_state.opcion_actual = unidad
                        st.session_state.vista_interna = "CONTACTO"
                        st.rerun()
                st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE ---
    else:
        opcion = st.session_state.opcion_actual
        vista = st.session_state.get("vista_interna", "FICHA")
        
        if st.button("← Volver al Menú Principal"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        if vista == "FICHA":
            st.subheader(f"Análisis Técnico: {opcion}")
            if opcion in diccionario_hojas:
                df = diccionario_hojas[opcion]
                df_clean = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

                # Formato de miles y sin decimales
                cols_numericas = df_clean.select_dtypes(include=['number']).columns
                st.dataframe(
                    df_clean, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        col: st.column_config.NumberColumn(format="%d") for col in cols_numericas
                    }
                )
                
                # --- AJUSTE DE TAMAÑO DE IMAGEN ---
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    # Quitamos el 'use_container_width' y definimos un ancho fijo
                    st.image(ruta_img, width=200) 
            else:
                st.error("Hoja no encontrada.")        
        else: # Vista CONTACTO
            st.subheader(f"Datos de Contacto: {opcion}")
            if "Contacto" in diccionario_hojas:
                df_c = diccionario_hojas["Contacto"]
                # Filtro por propiedad si existe la columna
                df_res = df_c[df_c['Propiedad'] == opcion] if 'Propiedad' in df_c.columns else df_c
                st.table(df_res)
            else:
                st.info("Pestaña 'Contacto' no encontrada en el Excel.")
else:
    st.error("No se encontró el archivo 'Opciones_Deptos_LM.xlsx'.")
