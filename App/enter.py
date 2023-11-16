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
import atexit
# START LISTENING ON P2P SERVER


def run_p2pserver(p2pserver):
    print("Running p2p server")
    p2pserver.listen()

def run_background_task(background):
    print("Running background block proposer updation")
    background.run_forever()
    

def on_program_exit():
    print("Main program is exiting. Closing threads.")
    if hasattr(st.session_state, "p2pserver"):
        st.session_state.p2pserver.stop()
    if hasattr(st.session_state, "background"):
        st.session_state.background.stop()

def initialise(private_key=None):
    st.session_state.validator = False

    if not st.session_state.initialise:
        # st.set_option('on_close', on_program_exit)
        st.session_state.blockchain = Blockchain()
        st.session_state.transaction_pool = TransactionPool()
        st.session_state.wallet = Wallet(
            private_key=private_key, name=st.session_state.name, email=st.session_state.email
        )

        p2pserver = P2pServer(
            blockchain=st.session_state.blockchain, transaction_pool=st.session_state.transaction_pool, wallet=st.session_state.wallet,
            user_type=st.session_state.user_type
        )

        background_task = Background(
            p2pserver=p2pserver
        )

        st.session_state.p2pserver = p2pserver
        st.session_state.background = background_task

        p2p_thread = threading.Thread(
            target=run_p2pserver, args=(
                st.session_state.p2pserver,), daemon=True
        )

        background_thread = threading.Thread(
            target=run_background_task, args=(
                st.session_state.background,), daemon=True
        )

        p2p_thread.start()
        background_thread.start()

        st.session_state.initialise = True
        # atexit.register(on_program_exit)
        
        print("EVERYTHING INITIALIZED")

    else:
        print("Already initialized")


def enter():
    st.title("Choose Role to enter into Network")

    if st.button("Login/Signup as News Auditor in the Private Network."):
        st.session_state.user_type = "Auditor"
        change_screen("login")

    if st.button("Login/Signup as a Reader in the Public Network."):
        st.session_state.user_type = "Reader"
        change_screen("login")
