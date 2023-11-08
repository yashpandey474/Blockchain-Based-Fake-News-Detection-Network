import streamlit as st
from change_screen import *
from enter import *
import crypto_logic
import time

def login():
    st.title("Login")

    user_input = st.text_area("Enter your Private Key")

    if st.button("Continue"):

        if user_input:
            vc = crypto_logic.verify(user_input)

            if vc[0]:
                st.markdown(f'<span style="color:green"><b><i>{vc[1]}</b></i></span>', unsafe_allow_html=True)
                time.sleep(1)
                initialise(vc[2])
                change_screen("main_page")

            else:
                st.markdown(f'<span style="color:yellow"><b>{vc[1]}</b></span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:yellow"><b>Key Not Provided</b></span>', unsafe_allow_html=True)

    if st.button("Sign up"):
        change_screen("sign_up")

    # if st.button("Ba ck"):
    #     change_screen(st.session_state.previous_screen)
