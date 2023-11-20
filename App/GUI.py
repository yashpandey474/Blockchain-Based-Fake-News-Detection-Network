import streamlit as st
from pyblock.blockchain.blockchain import *
from pyblock.blockchain.block import *
from pyblock.blockchain.account import *
import change_screen

import asyncio

background_style = '''<style>
div .appview-container{
background-image: url("https://i.gifer.com/5ARz.gif");
background-size: cover;
background-position: center;
}
</style>
'''

def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen in change_screen.screen_functions:
        change_screen.screen_functions[st.session_state.screen]()
        t = st.empty()
        change_screen.add_space()
        change_screen.add_space()
        st.session_state.screen_changed = False       
        asyncio.run(change_screen.watch(t))
        
    else:
        change_screen.screen_functions["enter"]()


        

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown(background_style, unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center;'>Fake News Detection System Utilising Blockchain</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <style>
    .stButton>button {
        width: 350px;
        height: 100px;
        text-align: center;
        display: block;
        margin: 0 auto;
        padding: 0;
    }
    .stButton p{
        font-size: 20px;
        style: bold;
        font-weight: 800;
        font-family: "Calibri";
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
    
    if "screen" not in st.session_state:
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.user_type = ""
        st.session_state.initialise = False
        st.session_state.validator = False
        st.session_state.previous_screen = "enter"
        st.session_state.screen = "enter"
        st.session_state.screen_changed = False
    
    main()

    
