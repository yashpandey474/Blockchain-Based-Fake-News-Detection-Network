# STREAMLIT GUI
import streamlit as st
import change_screen
from pyblock.wallet.transaction import *
from pyblock.blockchain.block import *
from pyblock.config import *
from datetime import datetime
import asyncio

def reader_navbar():
    return 


def main_page():
    user_type = st.session_state.user_type
    st.write("Welcome, " + st.session_state.name)
    # nav_selection = st.sidebar.selectbox("Navigation", change_screen.navigation_options.get(st.session_state.user_type, ()))
    # if nav_selection:
    #     change_screen.change_screen_navbar(nav_selection)
    if user_type == "Auditor":
        st.write("""As an auditor, you participate in our trusted private network. 
                     You must stake some "reputation" to become a validtor in the network. 
                     If you are chosen as a block proposing validator, you must choose some
                     transactions to include in a new block which is transmitted to other validators
                     and if  >=50\% of validators want the block to be included in the chain, it is added 
                     and you are rewarded with some reputation value. As a validator, you
                     would also (in addition to being in contention for becoming a block proposer) 
                     be able to vote on news in incoming blocks that other auditors chose to include 
                     as "Fake" or "True". A machine learning model is deployed that provides a
                     score from 0 to 1 as the probability of the news being fake according to our training data, this score
                     along with the reputation of the sender is available with every news received.
                     """)
        
    
        