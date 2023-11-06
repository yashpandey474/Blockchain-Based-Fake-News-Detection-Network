# CHANGE THE SCREEN OF GUI
import streamlit as st

def change_screen(input_string):
    st.session_state.previous_screen = st.session_state.screen
    st.session_state.screen = input_string
    st.rerun()
