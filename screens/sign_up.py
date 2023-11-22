import streamlit as st
import re
from extra import crypto_logic
from enter import initialise
import screens.change_screen as change_screen_
import time

def sign_up_generate():
    
    if st.session_state.screen == "sign_up_generate":
        st.markdown(
            f"<h1 style='text-align: center;'>Sign Up as a {st.session_state.user_type}</h1>",
            unsafe_allow_html=True
        )

        # Add buffer text to span the whole page
        col1, col2, col3 = st.columns([1, 20, 1])
        with col2:
            if st.session_state.user_type == "Auditor":
                st.write(change_screen_.auditors_guidelines)  # Modify this with your intended text
                
            else:
                st.markdown(change_screen_.readers_guidelines)

        # GENERATE A NEW PRIVATE KEY FOR USER
        if st.button("Generate a new Private Key"):
            st.session_state.gen_key_pressed = True
            
            with st.spinner("Generating Key"):
                st.session_state.private_key = crypto_logic.gen_sk()
            st.success("Generated Private key. Please store it safely.")

            # PRINT THE PRIVATE KEY
            with st.expander("Click to view private key"):
                kk = st.session_state.private_key.export_key().decode()
                kk = kk.replace("\n", "<br>")
                st.markdown(kk, unsafe_allow_html=True)

            # INITIALISE ACCOUNT & WALLET OF SESSION
        if st.session_state.gen_key_pressed:
            if st.button("Go to main"):
                
                with st.spinner("Initialising Server"):
                    initialise(st.session_state.private_key)
                    while not st.session_state.p2pserver.initialised:
                        pass
                
                    st.write("Server Initialised. Waiting for connections..")
                progress_bar = st.progress(0)
                for i in range(1, 101): 
                    time.sleep(0.02)  
                    progress_bar.progress(i)
                    
                change_screen_.change_screen("main_page")
                st.session_state.gen_key_pressed = False

        if st.button("Back"):
            with st.spinner("Please Wait"): 
                change_screen_.change_screen("sign_up")
                

def sign_up():
    if st.session_state.screen == "sign_up":
        st.title("Sign Up as a " + st.session_state.user_type)

        default_name = "Enter Name"
        default_email = "email@service.domain"
        default_certificate_id = "ABCD"

        name = st.text_input("Enter Your Name", value=default_name)
        email = st.text_input("Enter Your Email", value=default_email)

        if st.session_state.user_type == "Auditor":
            certificate_id = st.text_area(
                "Enter the SGX Certificate ID", value=default_certificate_id)

        if st.button("Submit Details"):
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(pattern, email):
                st.warning("Invalid Email ID")
                
            else:
                if st.session_state.user_type == "Auditor" and not crypto_logic.verify_certificate(certificate_id):
                    st.warning("Invalid Certificate ID")
                else:
                    st.session_state.name = name
                    st.session_state.email = email
                    with st.spinner("Please Wait"):
                         change_screen_.change_screen("sign_up_generate")

        # GO TO PREVIOUS SCREEN
        if st.button("Back"):
            with st.spinner("Please Wait"):
                 change_screen_.change_screen("login")
            