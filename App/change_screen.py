# CHANGE THE SCREEN OF GUI
import streamlit as st

def change_screen(input_string):
    
    if input_string == "enter":
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.initialise = False
        st.session_state.user_type = ""
        
    st.session_state.previous_screen = st.session_state.screen
    st.session_state.screen = input_string
    st.rerun()
