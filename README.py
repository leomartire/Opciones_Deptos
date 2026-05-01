/* Estilo para los botones de las filas (VER) */
    .stButton>button {
        height: 24px !important; /* Más bajo que antes */
        width: 60px !important;  /* Más angosto */
        font-size: 9px !important; /* Fuente sutil */
        border: 1px solid #d4af37 !important; 
        background-color: transparent !important;
        border-radius: 2px !important;
        color: #1a1a1a;
        padding: 0px !important;
        line-height: 1 !important;
    }

    /* Estilo para el botón de VOLVER (que debe ser más cómodo de tocar) */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton>button {
        height: 35px !important;
        width: 100% !important;
        font-size: 11px !important;
        margin-top: 20px;
    }
