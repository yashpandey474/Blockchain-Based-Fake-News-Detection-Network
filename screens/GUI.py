import sys
sys.path.append(".")

import change_screen as change_screen_
import asyncio

from account_info import show_account_info
from become_validator import become_validator
from vote_on_block import vote_on_block
from upload_file import upload_file
from view_sent_news import view_sent_news
from sign_up import sign_up, sign_up_generate
from enter import enter
from view_block_status import view_block_status, propose_block
from view_sent_blocks import view_sent_blocks
from view_log_reputation import view_log_reputation
from login import login
from main_page import main_page
from view_block_news import show_blocks_news
from show_transactions import show_transactions

import streamlit as st

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
    "view_block_status": view_block_status,
    "propose_block": propose_block,
    "view_sent_blocks": view_sent_blocks,
    "view_log_reputation": view_log_reputation
}



def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen in screen_functions:
        screen_functions[st.session_state.screen]()
        t = st.empty()
        change_screen_.add_space()
        change_screen_.add_space()
        st.session_state.screen_changed = False       
        asyncio.run(change_screen_.watch(t))
        
    else:
        screen_functions["enter"]()


        

if __name__ == "__main__":
    st.set_page_config(layout="wide")

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
    
    div .appview-container {
            background-image: url("https://i.gifer.com/5ARz.gif");
            background-size: cover;
            background-position: center;
    }
    
    .st-dh {
            border-color: red; /* Change 'red' to the color you want */
            border-left-color: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True
    )
    
    
    
    
    if "screen" not in st.session_state:
        st.session_state.main_pressed = False
        st.session_state.stake_submitted = False
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

    
