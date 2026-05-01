# 3. CSS REFORZADO CON MARGEN DINÁMICO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&display=swap');
    
    /* ADVERTENCIA DE ROTACIÓN */
    .orientacion-mensaje {
        display: none;
        background-color: #1a1a1a;
        color: #d4af37;
        text-align: center;
        padding: 15px;
        font-family: sans-serif;
        font-weight: bold;
        font-size: 13px;
        border-bottom: 2px solid #d4af37;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 999999;
    }

    /* Solo afecta a móviles en vertical */
    @media only screen and (max-width: 900px) and (orientation: portrait) {
        .orientacion-mensaje {
            display: block !important;
        }
        /* Aumentamos el margen superior para que el banner no tape la imagen */
        .stApp { 
            margin-top: 60px !important; 
        } 
    }

    /* DISEÑO PARA COMPUTADORA O MODO APAISADO (No se ve afectado) */
    @media only screen and (min-width: 901px), (orientation: landscape) {
        .stApp { 
            margin-top: -85px !important; 
        }
    }

    .block-container {
        padding-top: 0rem !important;
        max-width: 450px !important; 
        margin: 0 auto !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    
    /* Resto de los estilos se mantienen igual... */
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
    .stButton>button {
        height: 30px !important; font-size: 10px !important;
        border: 1px solid #d4af37 !important; background-color: transparent !important;
        width: 100% !important; border-radius: 4px; color: #1a1a1a;
    }
    .boton-aviso {
        display: block; width: 100%; text-align: center;
        background-color: transparent; border: 1px solid #d4af37;
        color: #1a1a1a; padding: 8px 0; border-radius: 4px;
        font-size: 11px; text-decoration: none; font-family: sans-serif;
        margin-top: 10px; font-weight: 500;
    }
    </style>
    
    <div class="orientacion-mensaje">
        🔄 POR FAVOR, GIRE SU PANTALLA (MODO APAISADO)
    </div>
    """, unsafe_allow_html=True)
