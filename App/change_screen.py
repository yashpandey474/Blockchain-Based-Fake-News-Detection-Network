# CHANGE THE SCREEN OF GUI
import streamlit as st
from pyblock.config import *
from account_info import *
from become_validator import *
from vote_on_block import *
from upload_file import *
from view_sent_news import *
from sign_up import *
from view_block_status import *
from view_sent_blocks import *
from view_log_reputation import *
from login import *
from main_page import *
from show_block_news import *
from show_transactions import *
from enter import *
import time
import asyncio

auditors_guidelines =         """
        ### Auditor Guidelines
        
        As an auditor, you play a vital role in our trusted private network. Here's what you do:
        
        - **Stake Reputation:** Stake some "reputation" to become a validator in the network.
        
        - **Block Proposal:** If chosen as a block proposing validator, select transactions for a new block. If the majority of validators (>50%) agree, the block is added, and you earn reputation.
        
        - **Voting on News:** Vote on news in incoming blocks labeled "Fake" or "True". A machine learning model provides a score (0-1) for the probability of fake news, alongside the sender's reputation.
        
        Your contributions help maintain network integrity and ensure the authenticity of shared news.
"""
    

readers_guidelines = """
### Guidelines for Readers:

As a reader in our network, you have the privilege to access and explore the news posted on our consortium blockchain. Here's what you can do:

1. **Anonymous Exploration:** Anonymously view news posted on the network without the need for authentication.

2. **Access Metrics:** Access essential information about news posts, including title, content, machine learning model score indicating the probability of fake news, percentage of auditors who voted the news as fake, and sender reputation.

3. **Stay Informed:** Engage with informative news content while being aware of the authenticity metrics provided.

4. **Contribute to Data Availability:** Contribute indirectly by generating data through your viewership, aiding in the creation of a more informed network environment.
"""

# General Message for the Enter Page
enter_page_message = """
### Welcome to our Consortium Blockchain Network!

Explore, learn, and engage responsibly with the news shared on our network. Anonymously browse through the latest posts and stay informed about each news item's authenticity metrics. Your viewership contributes to the generation of a transparent and informed network environment.

Discover the power of reliable information dissemination and responsible engagement within our network. Dive in, explore, and be part of a community fostering informed insights!
"""

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
    "propose_block": propose_block,
    "view_sent_blocks": view_sent_blocks,
    "view_log_reputation": view_log_reputation
}

entered_pages = set([
    "main_page",
    "account_info",
    "show_transac"
    "show_blocks",
    "become_validator",
    "vote_on_block",
    "upload_file",
    "view_sent_news",
    "vote_on_block",
    "view_block_status",
    "propose_block",
    "view_sent_blocks",
    "view_log_reputation"
])


if "validator" not in st.session_state:
    st.session_state.validator = False
    
navigation_options = {
    "Reader": ("Main Page", "Upload News", "View Verified News", "View Account Info", "View Sent News", "View Reputation Log", "Enter Page"),
    "Auditor": (
        "Main Page", "Upload News", "Verified News", "Account Info", "Sent News", "Reputation Log", "Transactions in Mempool",
        ("Modify Stake" if st.session_state.validator else "Become a Validator"),
        "Current Block Status", "Broadcasted Blocks",
        "Enter Page"
    )
}

screen_mapping = {
        "Main Page": "main_page",
        "Upload News": "upload_file",
        "Verified News": "show_blocks",
        "View Account Info": "account_info",
        "Sent News": "view_sent_news",
        "Reputation Log": "view_log_reputation",
        "Transactions in Mempool": "show_transac",
        "Modify Stake": "become_validator",
        "Become a Validator": "become_validator",
        "Current Block Status": "view_block_status",
        "Broadcasted Blocks": "view_sent_blocks",
        "Enter Page": "enter"
    }

def add_space():
    #ADD SPACE
    for i in range(30):
        st.empty()
        
def change_screen_navbar(nav_selection):    
        # Map the nav_selection to corresponding actions
    screen = screen_mapping.get(nav_selection)

    if screen:
        if nav_selection == "Modify Stake" or nav_selection == "Become a Validator":
            st.session_state.stake_submitted = False
            
        if nav_selection == "Upload News":
            st.session_state.upload_file_executed = False

        with st.spinner("Please Wait"):
            change_screen(screen)
            
async def watch(test):
    while True:
        if st.session_state.screen_changed:
            break
        
        current_time = int(time.time())
        time_elapsed = current_time - START_TIME.timestamp()
        time_remaining = BLOCK_VALIDATOR_CHOOSE_INTERVAL - (time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL)
        test.markdown(
            f"""
            <div class="time" style="font-size: 25px;text-align: center;color: black; background-color: white; style:bold;">
                Time Remaining in Current Block Proposing Period: {str(time_remaining)}
            </div>
            """, unsafe_allow_html=True)
        await asyncio.sleep(1)
        
def change_screen(input_string):
    print("CHANGE SCREEN CALLED ", input_string)
    if input_string == "enter":
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.initialise = False
        st.session_state.user_type = "Reader"
    
    st.session_state.screen_changed = True
    st.session_state.previous_screen = st.session_state.screen
    st.session_state.screen = input_string
    st.rerun()
