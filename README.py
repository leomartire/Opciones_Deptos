else:
        # --- VISTA FICHA TÉCNICA ---
        opcion = st.session_state.opcion_actual
        img_ficha = get_base64(f"images/{opcion}.png")
        if img_ficha:
            st.markdown(f'<div class="hero-container-ficha"><img src="data:image/png;base64,{img_ficha}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 class='titulo-elegante'>{opcion}</h1>", unsafe_allow_html=True)
        
        if opcion in diccionario_hojas:
            df_ficha = diccionario_hojas[opcion].copy()
            url_aviso = None
            
            for col in df_ficha.columns:
                mask = df_ficha[col].str.contains("http|www", na=False)
                if mask.any():
                    url_aviso = df_ficha.loc[mask, col].values[0]
                    df_ficha.loc[mask, col] = pd.NA 
                    break
            
            st.table(df_ficha.iloc[1:].dropna(how='all'))
            
            if url_aviso:
                st.markdown(f'<a href="{url_aviso}" target="_blank" class="boton-aviso">VER AVISO</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- NUEVA SECCIÓN DE BOTONES ALINEADOS ---
        col_volver, col_ws = st.columns(2)
        
        with col_volver:
            if st.button("← VOLVER", key="btn_back_final"):
                st.session_state.opcion_actual = "HOME"
                st.rerun()
        
        with col_ws:
            # Configuración del mensaje de WhatsApp
            telefono = "5491168807566" # Tu contacto profesional configurado
            mensaje = f"Hola! Me interesa obtener más información sobre la propiedad: {opcion}"
            mensaje_url = mensaje.replace(" ", "%20")
            ws_link = f"https://wa.me/{telefono}?text={mensaje_url}"
            
            # Botón estilizado para WhatsApp
            st.markdown(f"""
                <a href="{ws_link}" target="_blank" style="text-decoration: none;">
                    <div style="
                        height: 24px;
                        background-color: #25D366;
                        color: white;
                        text-align: center;
                        line-height: 24px;
                        border-radius: 2px;
                        font-family: sans-serif;
                        font-size: 9px;
                        font-weight: bold;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        cursor: pointer;
                        border: none;
                    ">
                        WhatsApp
                    </div>
                </a>
            """, unsafe_allow_html=True)
