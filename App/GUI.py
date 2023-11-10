import streamlit as st
from pyblock.blockchain.blockchain import *
from pyblock.blockchain.block import *
from pyblock.blockchain.account import *
from login import *
from main_page import *
from show_block_news import *
from show_transactions import *
from enter import *
from change_screen import *
from account_info import *
from become_validator import *
from vote_on_block import *
from upload_file import *
from view_sent_news import *
from sign_up import *
from view_block_status import *

background_style = '''<style>
div .appview-container{
background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmxvY2tjaGFpbnxlbnwwfHwwfHx8MA%3D%3D");
background-size: cover;
background-position: center;
width: 100%;
height: 100vh;
}
</style>
'''

st.markdown(background_style, unsafe_allow_html=True)
st.title("Fake News Detection System Utilising Blockchain")

screen_functions = {
    "enter": enter,
    "login": login,
    "main_page": main_page,
    "account_info": show_account_info,
    "show_transac": show_transactions,
    "show_blocks": show_blocks_news,
    "sign_up": sign_up,
    "sign_up_generate": sign_up_generate,
    "become_validator": become_validator,
    "vote_on_block": vote_on_block,
    "upload_file": upload_file,
    "view_sent_news": view_sent_news,
    "vote_on_block": vote_on_block,
    "view_block_status": view_block_status,
    "propose_block": propose_block
}

def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen in screen_functions:
        screen_functions[st.session_state.screen]()
    
    else:
        screen_functions["enter"]()
        

if __name__ == "__main__":
    if "screen" not in st.session_state:
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.initialise = False
        
        print("SCREEN INITILIASED")
        st.session_state.previous_screen = "enter"
        st.session_state.screen = "enter"
        
        
    main()
        
