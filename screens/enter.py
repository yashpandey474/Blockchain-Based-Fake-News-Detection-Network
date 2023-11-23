import streamlit as st
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from wallet.transaction_pool import TransactionPool
from p2p.p2pserver import P2pServer
import threading
from background import Background
import screens.change_screen as change_screen_


# START LISTENING ON P2P SERVER

def run_p2pserver(p2pserver):
    print("Running p2p server")
    p2pserver.start_server()


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

        print("EVERYTHING INITIALIZED")

    else:
        print("Already initialized")


def enter():

    if st.session_state.screen == "enter":
        st.markdown(
            f"<h2 style='text-align: center;'>Choose a Role to Enter into Network</h2>",
            unsafe_allow_html=True
        )

        st.markdown(change_screen_.enter_page_message)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login/Signup as News Auditor in the Private Network."):
                st.session_state.user_type = "Auditor"
                with st.spinner("Please Wait"):
                    change_screen_.change_screen("login")

        with col2:
            if st.button("Login/Signup as a Reader in the Public Network."):
                st.session_state.user_type = "Reader"
                with st.spinner("Please Wait"):
                    change_screen_.change_screen("login")