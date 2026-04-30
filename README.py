import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gestión de Inversiones Inmobiliarias", 
    layout="wide", 
    page_icon="🏢"
)

# 2. ESTILO CSS PARA DETALLES (Sin romper el layout)
st.markdown("""
    <style>
    /* Reducimos el padding superior de la página */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* Forzamos que los textos de la tabla sean pequeños */
    .tabla-texto {
        font-size: 11px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }

    /* Botones pequeños y centrados */
    .stButton>button {
        height: 24px !important;
        padding: 0px 10px !important;
        font-size: 10px !important;
        min-height: 24px !important;
        width: 100% !important;
    }

    /* Ajuste para que las líneas divisorias no ocupen tanto espacio */
    hr { margin: 4px 0 !important; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS (Basado en tu archivo Excel)
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        if os.path.exists(archivo):
            # Leemos todas las hojas como strings para evitar problemas de formato
            return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
        return None
    except Exception:
        return None

diccionario_hojas = cargar_datos()

# 4. LÓGICA PRINCIPAL
if diccionario_hojas:
    # Mapeo de nombres de hojas para navegación
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # USAMOS COLUMNAS PARA COMPRIMIR TODO AL CENTRO (Evita que la imagen sea enorme)
        # En la PC, el contenido ocupará solo el centro (1.2 de 3 partes)
        col_izq, col_centro, col_der = st.columns([1, 1.2, 1])
        
        with col_centro:
            # Imagen de Home controlada
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
            
            st.markdown("<h3 style='text-align: center; font-size: 16px;'>Panel de Control</h3>", unsafe_allow_html=True)
            st.markdown("---")

            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"]
                unidades_vistas = set()

                # Encabezado de la tabla (usando columnas internas)
                h = st.columns([1, 0.7, 1.3], gap="small")
                h[0].markdown("<b style='font-size:11px;'>Unidad</b>", unsafe_allow_html=True)
                h[1].markdown("<b style='font-size:11px;'>Acción</b>", unsafe_allow_html=True)
                h[2].markdown("<div style='text-align:right'><b style='font-size:11px;'>Contacto</b></div>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)

                if df_home is not None:
                    for index, row in df_home.iterrows():
                        # Obtener nombre de unidad
                        val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                        
                        # Saltar filas vacías o encabezados del Excel
                        if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                            continue
                        
                        unidades_vistas.add(val_unidad)
                        
                        # Fila de datos estrecha
                        fila = st.columns([1, 0.7, 1.3], gap="small")
                        
                        with fila[0]:
                            st.markdown(f"<p class='tabla-texto'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                        
                        with fila[1]:
                            key_match = val_unidad.upper()
                            if key_match in hojas_reales:
                                if st.button("Ver", key=f"btn_{index}"):
                                    st.session_state.opcion_actual = hojas_reales[key_match]
                                    st.rerun()
                        
                        with fila[2]:
                            # El contacto suele estar en la tercera columna (índice 2)
                            val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row[2]) else "-"
                            st.markdown(f"<p class='tabla-texto' style='text-align:right'>{val_contacto}</p>", unsafe_allow_html=True)
                        
                        st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)

    # --- VISTA DE DETALLE (FICHA TÉCNICA) ---
    else:
        opcion = st.session_state.opcion_actual
        
        # Botón de volver arriba
        if st.button("← Volver al Panel"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()

        st.subheader(f"Ficha Técnica: {opcion}")
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].dropna(how='all', axis=0)
            
            # Layout de dos columnas: Tabla a la izquierda, Imagen a la derecha
            col_t, col_f = st.columns([1.2, 0.8], gap="medium")
            
            with col_t:
                st.table(df_ficha)
            
            with col_f:
                ruta_img = f"images/{opcion}.png"
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_container_width=True)
                else:
                    st.info(f"Sin imagen disponible para {opcion}")

else:
    st.error("No se pudo cargar el archivo 'Opciones_Deptos_LM.xlsx'. Verificá que esté en la raíz del proyecto.")
