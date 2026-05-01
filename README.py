import streamlit as st
import pandas as pd
import os
import base64

# 1. PROCESAMIENTO DE IMÁGENES
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

# --- 3. NAVEGACIÓN (Prioridad Absoluta al Parámetro URL) ---
if "unidad" in st.query_params:
    st.session_state.opcion_actual = st.query_params["unidad"]
elif "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');
    .stApp { margin-top: -70px; } 
    .block-container {
        padding-top: 2rem !important; max-width: 450px !important; 
        margin: 0 auto !important; padding-left: 10px !important; padding-right: 10px !important;
    }
    thead, tbody th { display: none !important; }
    .stButton>button {
        height: 32px !important; width: 100% !important; font-size: 10px !important; 
        border-radius: 4px !important; font-family: sans-serif !important; 
        text-transform: uppercase !important; background-color: #e0e0e0 !important; color: #1a1a1a !important;
    }
    .btn-whatsapp {
        height: 32px !important; background-color: #25D366 !important;
        color: white !important; text-align: center; line-height: 32px !important;
        border-radius: 4px; font-family: sans-serif; font-size: 10px !important;
        text-decoration: none; display: block; width: 100%; text-transform: uppercase;
    }
    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;
    }
    .texto-base { font-size: 11px !important; font-family: sans-serif !important; color: #444; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. CARGA DE DATOS ---
@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

if diccionario_hojas:
    # --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<img src="data:image/png;base64,{img_64}" style="width:100%; border-radius:0 0 10px 10px; margin-bottom:1rem;">', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)
        df_home = diccionario_hojas.get("HOME")
        if df_home is not None:
            for index, row in df_home.iterrows():
                u = str(row[0]).strip()
                if not u or u.upper() in ["UNIDAD", "HOME"] or u.isdigit(): continue
                col1, col2, col3 = st.columns([1.9, 0.7, 1.1]) 
                with col1: st.markdown(f"<p class='texto-base' style='line-height:32px;'>{u}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_{index}"):
                        st.session_state.opcion_actual = u
                        st.rerun()
                with col3: st.markdown(f"<p class='texto-base' style='text-align:right; line-height:32px;'>{str(row[2])}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    # --- VISTA FICHA (CON BÚSQUEDA TOLERANTE) ---
    else:
        busqueda = st.session_state.opcion_actual.strip().upper()
        nombre_hoja_final = None

        # Buscamos la hoja: Primero coincidencia exacta, luego coincidencia parcial
        for nombre_real in diccionario_hojas.keys():
            if busqueda == str(nombre_real).strip().upper():
                nombre_hoja_final = nombre_real
                break
        
        if not nombre_hoja_final: # Si no hubo exacta, buscamos si la URL es parte del nombre
            for nombre_real in diccionario_hojas.keys():
                if busqueda in str(nombre_real).strip().upper():
                    nombre_hoja_final = nombre_real
                    break

        if nombre_hoja_final:
            # 1. Imagen
            img_ficha = get_base64(f"images/{nombre_hoja_final}.png")
            if img_ficha:
                st.markdown(f'<img src="data:image/png;base64,{img_ficha}" style="width:100%; max-height:280px; object-fit:contain; margin-bottom:1rem;">', unsafe_allow_html=True)
            
            st.markdown(f"<h1 class='titulo-elegante'>{nombre_hoja_final}</h1>", unsafe_allow_html=True)
            
            # 2. Tabla
            df_ficha = diccionario_hojas[nombre_hoja_final].copy()
            st.table(df_ficha.iloc[1:].dropna(how='all'))
            
            # 3. Botones
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← VOLVER"):
                    st.session_state.opcion_actual = "HOME"
                    st.query_params.clear()
                    st.rerun()
            with c2:
                num_ws = "5491168807566"
                url_base = "https://inversiones-inmobiliarias.streamlit.app" # REVISAR ESTA URL
                link_f = f"{url_base}?unidad={nombre_hoja_final.replace(' ', '%20')}"
                link_ws = f"https://wa.me/{num_ws}?text=Me%20interesa:%20{link_f}"
                st.markdown(f'<a href="{link_ws}" target="_blank" class="btn-whatsapp">WhatsApp</a>', unsafe_allow_html=True)
        else:
            st.error(f"No se encontró la hoja: {busqueda}")
            if st.button("Volver al Inicio"):
                st.session_state.opcion_actual = "HOME"
                st.query_params.clear()
                st.rerun()
