import streamlit as st
from change_screen import *
from enter import *
import crypto_logic
import time

def login():
    
    st.title("Login as a " + st.session_state.user_type)

    #GET PRIVATE KEY OF USER
    user_input = st.text_area("Enter your Private Key")

    #SUBMIT
    if st.button("Submit key"):
        
        #IF PRIVATE KEY ENTERED
        if user_input:
            vc = crypto_logic.verify(user_input)

            if vc[0]:
                st.markdown(f'<span style="color:green"><b><i>{vc[1]}</b></i></span>', unsafe_allow_html=True)
                initialise(vc[2])
                change_screen("main_page")

            else:
                st.markdown(f'<span style="color:yellow"><b>{vc[1]}</b></span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:yellow"><b>Key Not Provided</b></span>', unsafe_allow_html=True)

    b1= st.button("New to app? Sign up instead")
    b2 = st.button("Exit Screen")
    
    if b1:
        change_screen("sign_up")
    elif b2:
        change_screen("enter")

    # if st.button("Ba ck"):
    #     change_screen(st.session_state.previous_screen)
