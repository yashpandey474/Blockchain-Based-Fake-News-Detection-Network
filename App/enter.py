import streamlit as st
from pyblock.blockchain.blockchain import Blockchain
from pyblock.blockchain.block import *
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
from pyblock.peers import *
import threading
from pyblock.blockchain.account import *
from change_screen import *
from background import *
# START LISTENING ON P2P SERVER


def run_p2pserver(p2pserver):
    print("Running p2p server on port: "+str(P2P_PORT))
    p2pserver.listen()


def initialise(private_key=None):
    st.session_state.validator = False

    st.session_state.block_proposer = None

    st.session_state.block_received = False

    st.session_state.received_block = None
    
    if "blockchain" not in st.session_state:
        st.session_state.blockchain = Blockchain()

        st.session_state.transaction_pool = TransactionPool()

        st.session_state.wallet = Wallet(
            private_key=private_key, name=st.session_state.name,
            email=st.session_state.email
        )

        print("P2P SERVER CALLED!")

        st.session_state.p2pserver = P2pServer(
            blockchain=st.session_state.blockchain, transaction_pool=st.session_state.transaction_pool, wallet=st.session_state.wallet
        )

        p2p_thread = threading.Thread(
            target=run_p2pserver, args=(st.session_state.p2pserver,)
        )

        p2p_thread.start()
        background_thread = threading.Thread(target=background_task)
        background_thread.start()
        
        print("EVERYTHING INITIIALISED")


def enter():
    st.title("Choose Role to enter into Network")

    if st.button("Login/Signup as News Auditor"):
        st.session_state.user_type = "Auditor"
        print("BUTTON CLICKED")
        change_screen("login")

    if st.button("Enter as a Reader."):
        st.session_state.user_type = "Reader"
        st.session_state.name = "User"
        st.session_state.email = None
        print("BUTTON CLICKED")
        initialise()

        change_screen("main_page")
