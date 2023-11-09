from pyblock.wallet.transaction import *
import streamlit as st
from change_screen import *
import binascii


def show_account_info():
    st.title("ACCOUNT INFORMATION")

    public_key = st.session_state.p2pserver.wallet.get_public_key()
    private_key = st.session_state.p2pserver.wallet.get_private_key()
    balance = st.session_state.blockchain.get_balance(
        public_key
    )
    stake = st.session_state.blockchain.get_stake(public_key)
    st.write("Current Balance = ", balance)
    if st.session_state.validator:
        st.write("Currrent Stake in Network = ", stake)
    st.write("PUBLIC KEY = ", public_key)
    st.write("PRIVATE KEY = ", private_key)

    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
