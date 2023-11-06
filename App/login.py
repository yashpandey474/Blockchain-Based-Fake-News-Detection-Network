import streamlit as st
from change_screen import *
from enter import *
import crypto_logic

def login():
    st.title("Login")

    user_input = st.text_area("Enter your Private Key")

    if st.button("Continue"):

        if user_input:
            vc = crypto_logic.verify(user_input)

            if vc[0]:
                initialise(vc[2])
                change_screen("main_page")

            else:
                st.write(vc[1])

    if st.button("Sign up"):
        change_screen("sign_up")

    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
