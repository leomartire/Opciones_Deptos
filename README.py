import streamlit as st
import pandas as pd
import os
import base64

# 1. CARGA DE IMÁGENES
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. CONFIGURACIÓN
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# 3. CSS (Corrección de puntero y ocultamiento de índices)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    .stApp { margin-top: -85px; }

    .block-container {
        padding-top: 0rem !important;
        max-width: 450px !important; 
        margin: 0 auto !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    /* OCULTAR NÚMEROS DE ÍNDICE Y CABECERAS TÉCNICAS */
    thead { display: none !important; }
    tbody th { display: none !important; }
    
    .hero-container-home, .hero-container-ficha {
        width: 100%; border-radius: 0 0 10px 10px; background-color: #f4f1ea;
        overflow: hidden; margin-bottom: 1rem;
    }
    .hero-container-home { height: 160px; }
    .hero-container-home img { width: 100%; height: 100%; object-fit: cover; }
    
    .hero-container-ficha { height: auto; max-height: 280px; display: flex; justify-content: center; }
    .hero-container-ficha img { max-width: 100%; max-height: 280px; object-fit: contain; }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;
    }

    .texto-base { font-size: 11px !important; font-family: sans-serif !important; color: #444; }

    /* Estilo de Botones Streamlit */
    .stButton>button {
        height: 30px !important; font-size: 10px !important;
        border: 1px solid #d4af37 !important; background-color: transparent !important;
        width: 100% !important; border-radius: 4px; color: #1a1a1a;
        cursor: pointer !important;
    }

    /* Estilo para el botón de VER AVISO */
    .boton-aviso {
        display: block; width: 100%; text-align: center;
        background-color: transparent; border: 1px solid #d4af37;
        color: #1a1a1a; padding: 8px 0; border-radius: 4px;
        font-size: 11px; text-decoration: none; font-family: sans-serif;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. DATOS
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

    # --- NAVEGACIÓN ---
    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container-home"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            unidades_vistas = set()
            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                # Filtro para quitar filas con números o textos de cabecera
                if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME", "0", "1", "2"] or val_unidad.isdigit():
                    continue
                unidades_vistas.add(val_unidad)
                
                col1, col2, col3 = st.columns([1.8, 0.7, 1.3]) 
                with col1: st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_h_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with col3:
                    val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    else:
        # --- VISTA FICHA TÉCNICA ---
        opcion = st.session_state.opcion_actual
        img_ficha = get_base64(f"images/{opcion}.png")
        if img_ficha:
            st.markdown(f'<div class="hero-container-ficha"><img src="data:image/png;base64,{img_ficha}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>{opcion}</h1>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].copy()
            # Buscamos si hay algún link en la tabla para extraerlo y luego limpiar la tabla
            url_encontrada = None
            for col in df_ficha.columns:
                for val in df_ficha[col]:
                    if isinstance(val, str) and ("http" in val or "www." in val):
                        url_encontrada = val
                        break
            
            # Limpieza: quitamos la primera fila (índices) y filas que contengan la URL
            df_mostrar = df_ficha.iloc[1:].replace(url_encontrada, pd.NA).dropna(how='all')
            st.table(df_mostrar)
            
            # Si es la ficha 8 o encontramos un link, mostramos el botón
            if "8" in opcion or url_encontrada:
                target_url = url_encontrada if url_encontrada else "#"
                st.markdown(f'<a href="{target_url}" target="_blank" class="boton-aviso">VER AVISO</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # BOTÓN VOLVER (Fuera de cualquier bloque de tabla para asegurar funcionamiento)
        if st.button("← VOLVER AL PANEL", key="back_btn"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
