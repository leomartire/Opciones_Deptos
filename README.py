import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Navegador de Propiedades", layout="wide", page_icon="🏠")

# Estilo personalizado para mejorar la visualización
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTable {
        background-color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar los datos del nuevo archivo
@st.cache_data
def cargar_datos():
    archivo = "Opciones_Deptos_LM.xlsx"
    try:
        # Cargamos todas las pestañas
        return pd.read_excel(archivo, sheet_name=None)
    except Exception as e:
        st.error(f"No se pudo encontrar el archivo {archivo}. Revisa el nombre en GitHub.")
        return None

diccionario_hojas = cargar_datos()

if diccionario_hojas:
    # --- NAVEGACIÓN (SIDEBAR) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
    st.sidebar.title("Inversiones Inmobiliarias")
    
    # Lista de pestañas disponibles
    nombres_hojas = list(diccionario_hojas.keys())
    opcion = st.sidebar.radio("Selecciona una opción:", nombres_hojas)

    # --- CUERPO PRINCIPAL ---
    st.title(f"📍 {opcion}")
    
    df = diccionario_hojas[opcion]

    # Limpiamos filas/columnas vacías que suele generar Excel
    df = df.dropna(how='all').dropna(axis=1, how='all')

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Dirección")
        # Mostramos la tabla (usamos table para que se vea fija y profesional)
        st.table(df)

        # Lógica para detectar Links (Zonaprop, etc)
        # Buscamos en el dataframe cualquier celda que contenga 'http'
        for r_idx, row in df.iterrows():
            for val in row:
                if isinstance(val, str) and "http" in val:
                    st.link_button(f"🔗 Ver publicación original", val, type="primary")

    with col2:
        st.subheader("Detalle")
        # Intentamos cargar la imagen desde la carpeta /fotos
        # El nombre del archivo debe ser igual al nombre de la pestaña + .jpg
        ruta_foto = f"images/{opcion}.png"
        
        if os.path.exists(ruta_foto):
            st.image(ruta_foto, caption=f"Propiedad: {opcion}", use_container_width=True)
        else:
            # Mensaje de ayuda si no encuentra la foto
            st.info(f"Para ver la imagen, sube un archivo llamado '{opcion}.jpg' a la carpeta 'images' en GitHub.")
            
    # Botón de retorno al Home si no estás en el Home
    if opcion != "HOME":
        # Título principal con estilo
        st.markdown("# 🏠 Buscador de Departamentos")
        st.markdown("### Bienvenido al tablero de control de propiedades")
        
        # Un mensaje de bienvenida amigable
        st.write("En este sitio puedes comparar las diferentes opciones que estamos evaluando. "
                 "Usa el menú de la izquierda para ver los detalles, fotos y links de cada propiedad.")

        st.divider() # Una línea divisoria estética

        # Mostramos la tabla general que tienes en tu Excel
        st.subheader("📋 Lista Comparativa")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Agregamos unas tarjetas con datos rápidos (Métricas)
        st.markdown("---")
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.metric(label="Propiedades en Lista", value=len(df))
        with col_m2:
            st.metric(label="Zona de Búsqueda", value="Capital Federal")

        st.info("💡 Consejo: Selecciona una dirección en el menú lateral para ver las fotos y el link al aviso.")

    else:
        # Aquí sigue el código de las otras pestañas (el que ya tienes)
       # --- SECCIÓN DE TÍTULOS Y CONTENIDO ---
if opcion == "HOME":
    # Todo esto tiene 4 espacios de sangría
    st.title("📊 Resumen de Búsqueda")
    st.markdown("### Bienvenido al análisis comparativo")
    
    # Si tienes una foto de portada, se muestra aquí
    ruta_home = "fotos/home_portada.jpg"
    if os.path.exists(ruta_home):
        st.image(ruta_home, use_container_width=True)
    
    st.write("Seleccioná un departamento en el menú de la izquierda para ver los detalles.")
    st.divider()
    st.subheader("📋 Lista Comparativa")
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    # Todo lo que está después del 'else' también lleva sangría
    st.title(f"📍 {opcion}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Ficha Técnica")
        df_clean = df.dropna(how='all').dropna(axis=1, how='all')
        st.table(df_clean)
        
        for row in df_clean.values:
            for cell in row:
                if isinstance(cell, str) and "http" in cell:
                    st.link_button("🌐 Ver publicación original", cell)

    with col2:
        st.subheader("Galería")
        ruta_foto = f"fotos/{opcion}.jpg"
        if os.path.exists(ruta_foto):
            st.image(ruta_foto, use_container_width=True)
        else:
            st.info(f"Falta subir la foto: {opcion}.jpg")
