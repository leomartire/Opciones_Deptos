# 2. ESTILO CSS REFINADO (Más pequeño, sin márgenes y responsive)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');

    /* Eliminar espacios en blanco superiores de Streamlit */
    .stApp {
        margin-top: -60px;
    }

    .block-container {
        padding-top: 0rem !important;
        max-width: 600px !important; /* Estrecho para que se vea bien en móvil */
        margin: 0 auto !important;
    }

    /* Contenedor del Banner - Tamaño reducido */
    .hero-container {
        width: 100%;
        height: 220px; /* Altura reducida para que no sea enorme */
        overflow: hidden;
        margin-bottom: 1.5rem;
        border-radius: 0 0 15px 15px; /* Bordes redondeados sutiles abajo */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .hero-container img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
        object-position: center;
    }

    /* Ajustes específicos para móviles */
    @media (max-width: 640px) {
        .hero-container {
            height: 160px; /* Más pequeña aún en teléfonos */
        }
        .titulo-elegante {
            font-size: 22px !important;
        }
        /* Forzar que las columnas no se rompan en móvil para mantener la línea */
        [data-testid="column"] {
            width: fit-content !important;
            flex: 1 1 auto !important;
        }
    }

    .titulo-elegante {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 26px !important;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* ... (resto de tus estilos de botones y tablas) */
    </style>
    """, unsafe_allow_html=True)
