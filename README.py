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

# 3. CSS FINAL (Limpieza absoluta de tablas e índices)
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

    /* OCULTAR NÚMEROS DE ÍNDICE Y CABECERAS */
    thead { display: none !important; }
    tbody th { display: none !important; }
    [data-testid="stTable"] { font-family: sans-serif !important; }
    
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

    .stButton>button {
        height: 30px !important; font-size: 10px !important;
        border: 1px solid #d4af37 !important; background-color: transparent !important;
        width: 100% !important; border-radius: 4px; color: #1a1a1a;
        cursor: pointer !important;
    }

    .boton-aviso {
        display: block; width: 100%; text-align: center;
        background-color: transparent; border: 1px solid #d4af37;
        color: #1a1a1a; padding: 8px 0; border-radius: 4px;
        font-size: 11px; text-decoration: none; font-family: sans-serif;
        margin-top: 10px; font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. DATOS
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        # Cargamos todas las hojas
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

if diccionario_hojas:
    # Mapeo de nombres para búsqueda insensible a mayúsculas
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    if "opcion_actual" not in st.session_state:
        st.session_state.opcion_actual = "HOME"

    # --- LÓGICA DE NAVEGACIÓN ---
    
    if st.session_state.opcion_actual == "HOME":
        # --- VISTA PANEL PRINCIPAL ---
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div class="hero-container-home"><img src="data:image/png;base64,{img_64}"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)

        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            unidades_vistas = set()
            st.markdown("<hr style='margin: 0 0 8px 0; opacity: 0.3; border-top: 1px solid #333;'>", unsafe_allow_html=True)
            
            for index, row in df_home.iterrows():
                val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                
                # FILTRADO CRÍTICO: Eliminamos "HOME", números de índice y celdas vacías
                if (val_unidad == "" or 
                    val_unidad.upper() in ["UNIDAD", "HOME", "0", "1", "2"] or 
                    val_unidad.isdigit() or 
                    val_unidad in unidades_vistas):
                    continue
                
                unidades_vistas.add(val_unidad)
                
                col1, col2, col3 = st.columns([1.8, 0.7, 1.3]) 
                with col1: 
                    st.markdown(f"<p class='texto-base'>{val_unidad}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_nav_{index}"):
                        st.session_state.opcion_actual = hojas_reales.get(val_unidad.upper(), "HOME")
                        st.rerun()
                with col3:
                    val_contacto = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    else:
        # --- VISTA FICHA TÉCNICA ---
        opcion = st.session_state.opcion_actual
        
        # Banner de la unidad
        img_ficha = get_base64(f"images/{opcion}.png")
        if img_ficha:
            st.markdown(f'<div class="hero-container-ficha"><img src="data:image/png;base64,{img_ficha}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>{opcion}</h1>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].copy()
            
            # Buscamos y extraemos cualquier URL para el botón
            url_aviso = None
            for col in df_ficha.columns:
                mask = df_ficha[col].str.contains("http|www", na=False)
                if mask.any():
                    url_aviso = df_ficha.loc[mask, col].values[0]
                    # Limpiamos la celda que tenía la URL para que no se vea el texto largo
                    df_ficha.loc[mask, col] = pd.NA
                    break
            
            # Mostramos la tabla (limpia de índices y encabezados técnicos)
            df_clean = df_ficha.iloc[1:].dropna(how='all')
            st.table(df_clean)
            
            # Botón "VER AVISO" si existe URL
            if url_aviso:
                st.markdown(f'<a href="{url_aviso}" target="_blank" class="boton-aviso">VER AVISO</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de retorno siempre operativo
        if st.button("← VOLVER AL PANEL", key="final_back_btn"):
            st.session_state.opcion_actual = "HOME"
            st.rerun()
else:
    st.error("Base de datos no encontrada.")
