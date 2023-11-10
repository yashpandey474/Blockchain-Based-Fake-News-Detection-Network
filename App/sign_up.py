import streamlit as st
from change_screen import *
from pyblock.chainutil import *
from enter import *
import crypto_logic
import re


def sign_up_generate():
    st.title("Sign Up as a " + st.session_state.user_type)
    print("session NAME = ", st.session_state.name)
    print("session EMAIL = ", st.session_state.email)

    #GENERATE A NEW PRIVATE KEY FOR USER
    if st.button("Click to generate a new private key"):
        st.session_state.gen_key_pressed = True

        st.markdown(
            "<span style='font-style: italic; color: #FF5733;'><b>Generating New key <br> store it for future use</b></span>",
            unsafe_allow_html=True
        )

        private_key = crypto_logic.gen_sk()
        
        #INITIALISE ACCOUNT & WALLET OF SESSION
        initialise(private_key)

        #PRINT THE PRIVATE KEY
        st.write(private_key.export_key().decode())


    if st.session_state.gen_key_pressed:
        if st.button("Go to main"):
            # st.session_state.gen_key_pressed = False
            change_screen("main_page")
            
    else:
        if st.button("Back"):
            change_screen("sign_up")
    
def sign_up():
    st.title("Sign Up as a " + st.session_state.user_type)

    name = st.text_input("Enter Your Name", st.session_state.name)
    email = st.text_input("Enter Your Email",st.session_state.email)
    
    #NEWS AUDITOR MUST BE AUTHORISED BY A TTP [SAY, INTEL SGX CERTIFICATES]
    # TODO: FINALISE VERIFICATION TECHNIQUE AND WHETHER TO ACTUALLY USE INTEL SGX
    
    if st.session_state.user_type == "Auditor":
        certificate_id = st.text_area("Enter the SGX Certificate ID")
    
    if st.button("Submit Details"):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            st.markdown('<span style="color:yellow"><b>Invalid Email ID</b></span>', unsafe_allow_html=True)

        else:
            if st.session_state.user_type == "Auditor" and not crypto_logic.verify_certificate(certificate_id):
                st.markdown('<span style="color:yellow"><b>Invalid Certificate ID</b></span>', unsafe_allow_html=True)
            
            else:
                st.session_state.name = name
                st.session_state.email = email
                change_screen("sign_up_generate")
            
    # GO TO PREVIOUS SCREEN
    if st.button("Back"):
        change_screen("login")
