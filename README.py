import streamlit as st
import pandas as pd
import os
import base64

# 1. FUNCIÓN PARA PROCESAR IMÁGENES LOCALES
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Zeylicovich & Arzumanián | Inversiones", 
    layout="wide", 
    page_icon="🏢"
)

# --- 3. CARGA DE DATOS (Necesaria antes de la navegación) ---
@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    if os.path.exists(archivo):
        # Cargamos todo el libro de Excel
        return pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    return None

diccionario_hojas = cargar_datos()

# --- 4. LÓGICA DE NAVEGACIÓN ---
# Verificamos si hay una unidad en la URL
query_params = st.query_params
if "unidad" in query_params:
    st.session_state.opcion_actual = query_params["unidad"]
elif "opcion_actual" not in st.session_state:
    st.session_state.opcion_actual = "HOME"

# --- 5. ESTILOS CSS ---
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
        height: 32px !important; width: 100% !important;
        font-size: 10px !important; border-radius: 4px !important;
        font-family: sans-serif !important; font-weight: 600 !important;
        text-transform: uppercase !important; border: none !important; 
        background-color: #e0e0e0 !important; color: #1a1a1a !important;
    }
    .btn-whatsapp {
        height: 32px !important; background-color: #25D366 !important;
        color: white !important; text-align: center; line-height: 32px !important;
        border-radius: 4px; font-family: sans-serif; font-size: 10px !important;
        font-weight: 600; text-transform: uppercase; text-decoration: none; display: block; width: 100%;
    }
    .boton-aviso {
        display: block; width: 100%; height: 32px !important;
        line-height: 32px !important; text-align: center;
        background-color: #e0e0e0 !important; color: #1a1a1a !important;
        border-radius: 4px; font-size: 10px !important;
        text-decoration: none; font-family: sans-serif; margin-top: 10px;
        font-weight: 600; text-transform: uppercase;
    }
    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important; color: #1a1a1a; text-align: center;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;
    }
    .texto-base { font-size: 11px !important; font-family: sans-serif !important; color: #444; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

if diccionario_hojas:
    # Mapeo para normalizar nombres de hojas
    hojas_reales = {str(k).strip().upper(): k for k in diccionario_hojas.keys()}
    
    # --- VISTA: HOME ---
    if st.session_state.opcion_actual == "HOME":
        img_64 = get_base64("images/HOME.png")
        if img_64:
            st.markdown(f'<div style="width:100%; border-radius:0 0 10px 10px; overflow:hidden; margin-bottom:1rem;"><img src="data:image/png;base64,{img_64}" style="width:100%;"></div>', unsafe_allow_html=True)
        
        st.markdown("<h1 class='titulo-elegante'>Inversiones 2026</h1>", unsafe_allow_html=True)
        df_home = diccionario_hojas.get("HOME")
        
        if df_home is not None:
            st.markdown("<hr style='margin: 0 0 8px 0; opacity: 0.3;'>", unsafe_allow_html=True)
            for index, row in df_home.iterrows():
                val_raw = str(row[0]).strip() if pd.notnull(row[0]) else ""
                if not val_raw or val_raw.upper() in ["UNIDAD", "HOME"] or val_raw.isdigit():
                    continue
                
                col1, col2, col3 = st.columns([1.9, 0.7, 1.1]) 
                with col1: 
                    st.markdown(f"<p class='texto-base' style='line-height:32px;'>{val_raw}</p>", unsafe_allow_html=True)
                with col2:
                    if st.button("VER", key=f"btn_{index}"):
                        nombre_final = hojas_reales.get(val_raw.upper(), val_raw)
                        st.session_state.opcion_actual = nombre_final
                        st.query_params["unidad"] = nombre_final
                        st.rerun()
                with col3:
                    val_cont = str(row[2]).strip() if len(row) > 2 else "-"
                    st.markdown(f"<p class='texto-base' style='text-align:right; line-height:32px;'>{val_cont}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; opacity:0.1;'>", unsafe_allow_html=True)

    # --- VISTA: FICHA TÉCNICA ---
    else:
        # Recuperamos el nombre de la unidad (asegurándonos que coincida con el Excel)
        opcion_solicitada = st.session_state.opcion_actual.strip().upper()
        nombre_hoja = hojas_reales.get(opcion_solicitada, st.session_state.opcion_actual)
        
        # 1. Imagen Hero
        img_ficha = get_base64(f"images/{nombre_hoja}.png")
        if img_ficha:
            st.markdown(f'<div style="width:100%; max-height:280px; overflow:hidden; display:flex; justify-content:center; margin-bottom:1rem;"><img src="data:image/png;base64,{img_ficha}" style="max-width:100%; object-fit:contain;"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>{nombre_hoja}</h1>", unsafe_allow_html=True)
        
        # 2. Render de la Tabla (La Ficha Técnica)
        if nombre_hoja in diccionario_hojas:
            df_ficha = diccionario_hojas[nombre_hoja].copy()
            # Limpieza de links
            url_aviso = None
            for col in df_ficha.columns:
                mask = df_ficha[col].str.contains("http|www", na=False)
                if mask.any():
                    url_aviso = df_ficha.loc[mask, col].values[0]
                    df_ficha.loc[mask, col] = pd.NA 
                    break
            
            # Mostramos la tabla solo si tiene contenido
            st.table(df_ficha.iloc[1:].dropna(how='all'))
            
            if url_aviso:
                st.markdown(f'<a href="{url_aviso}" target="_blank" class="boton-aviso">VER AVISO PUBLICADO</a>', unsafe_allow_html=True)
        else:
            st.error(f"No se encontró información para: {nombre_hoja}")

        # 3. Botones de Acción
        st.markdown("<br>", unsafe_allow_html=True)
        col_volver, col_ws = st.columns(2)
        
        with col_volver:
            if st.button("← VOLVER", key="btn_back"):
                st.session_state.opcion_actual = "HOME"
                st.query_params.clear()
                st.rerun()
        
        with col_ws:
            num_ws = "5491168807566"
            # Reemplaza con tu URL real de Streamlit
            url_base = "https://tu-app-revaloriza.streamlit.app" 
            link_ficha = f"{url_base}?unidad={nombre_hoja.replace(' ', '%20')}"
            txt_ws = f"Hola! Me interesa esta propiedad: {link_ficha}"
            link_ws = f"https://wa.me/{num_ws}?text={txt_ws.replace(' ', '%20')}"
            st.markdown(f'<a href="{link_ws}" target="_blank" class="btn-whatsapp">WhatsApp</a>', unsafe_allow_html=True)
            st.markdown(f'<a href="{link_ws}" target="_blank" class="btn-whatsapp">WhatsApp</a>', unsafe_allow_html=True)
