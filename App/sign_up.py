import streamlit as st
from change_screen import *
from enter import *
import crypto_logic
def sign_up():
    st.title("Sign Up")

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
