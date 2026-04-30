# --- VISTA HOME ---
    if st.session_state.opcion_actual == "HOME":
        # 1. CONTENEDOR DE CENTRADO (Esto achica todo en la PC)
        # Usamos [1, 1.2, 1] para que el centro sea angosto y profesional
        col_espacio_izq, col_contenido, col_espacio_der = st.columns([1, 1.2, 1])
        
        with col_contenido:
            # IMAGEN (Ahora controlada por el ancho de col_contenido)
            if os.path.exists("images/HOME.png"):
                st.image("images/HOME.png", use_container_width=True)
            
            st.markdown("<h3 style='text-align: center; font-size: 16px;'>Panel de Control</h3>", unsafe_allow_html=True)
            st.markdown("---")

            if "HOME" in diccionario_hojas:
                df_home = diccionario_hojas["HOME"]
                unidades_vistas = set()

                # ENCABEZADO DE TABLA (Muy compacto)
                h = st.columns([1, 0.7, 1.3], gap="small")
                h[0].markdown("<b style='font-size:11px;'>Unidad</b>", unsafe_allow_html=True)
                h[1].markdown("<b style='font-size:11px;'>Acción</b>", unsafe_allow_html=True)
                h[2].markdown("<div style='text-align:right'><b style='font-size:11px;'>Contacto</b></div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

                if df_home is not None:
                    for index, row in df_home.iterrows():
                        val_unidad = str(row[0]).strip() if pd.notnull(row[0]) else ""
                        
                        if val_unidad == "" or val_unidad.upper() in ["UNIDAD", "HOME"] or val_unidad in unidades_vistas:
                            continue
                        unidades_vistas.add(val_unidad)
                        
                        # FILA DE DATOS
                        fila = st.columns([1, 0.7, 1.3], gap="small")
                        
                        with fila[0]:
                            st.markdown(f"<p style='font-size:11px; margin:0;'><b>{val_unidad}</b></p>", unsafe_allow_html=True)
                        
                        with fila[1]:
                            key_match = val_unidad.upper()
                            if key_match in hojas_reales:
                                # Botón pequeño para no estirar la fila
                                if st.button("Ver", key=f"btn_{index}"):
                                    st.session_state.opcion_actual = hojas_reales.get(key_match, "HOME")
                                    st.rerun()
                        
                        with fila[2]:
                            val_contacto = str(row[2]).strip() if len(row) > 2 and pd.notnull(row.iloc[2]) else "-"
                            # Alineado a la derecha para que se vea ordenado
                            st.markdown(f"<p style='font-size:11px; margin:0; text-align:right;'>{val_contacto}</p>", unsafe_allow_html=True)
                        
                        st.markdown("<hr style='margin: 2px 0; opacity: 0.1;'>", unsafe_allow_html=True)
