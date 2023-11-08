import streamlit as st
from change_screen import *
from pyblock.chainutil import *
from enter import *
import crypto_logic


def sign_up_generate():
    print("NAME = ", st.session_state.name)
    print("EMAIL = ", st.session_state.email)
    
    if st.button("Gen new key"):
        st.write("new key, wont see again, keep for future")

        private_key = crypto_logic.gen_sk()

        st.session_state.initialise = True

        initialise(private_key)

        st.write(private_key.export_key().decode())

        st.session_state.gen_key_pressed = True

    if st.session_state.gen_key_pressed:
        if st.button("Go to main"):
            print("BUTTON CLICKED")
            change_screen("main_page")
            
    # GO TO PREVIOUS SCREEN
    if st.button("Back"):
        change_screen("sign_up")
    
def sign_up():
    st.title("Sign Up As a News Auditor")
    
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Professional Email")
    
    #NEWS AUDITOR MUST BE AUTHORISED BY A TTP [SAY, INTEL SGX CERTIFICATES
    # TODO: FINALISE VERIFICATION TECHNIQUE AND WHETHER TO ACTUALLY USE INTEL SGX
    certificate_id = st.text_area("Enter the SGX Certificate ID")
    
    if st.button("Submit Details"):
        
        if not crypto_logic.verify_certificate(certificate_id):
            st.markdown('<span style="color:yellow"><b>Invalid Certificate ID</b></span>', unsafe_allow_html=True)
        
        else:
            st.session_state.name = name
            st.session_state.email = email
            change_screen("sign_up_generate")
            
    # GO TO PREVIOUS SCREEN
    if st.button("Back"):
        change_screen("login")
