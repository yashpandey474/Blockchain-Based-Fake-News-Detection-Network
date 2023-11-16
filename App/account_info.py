from pyblock.wallet.transaction import *
import streamlit as st
from change_screen import *

copy_to_clipboard_js = """
function copyTextToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            console.log("Text copied to clipboard");
            alert("Private key copied to clipboard!");
        })
        .catch(err => {
            console.error("Error in copying text: ", err);
            alert("Failed to copy private key!");
        });
}
"""


def show_account_info():
    st.title("ACCOUNT INFORMATION")
    #GET USER'S DETAILS
    public_key = st.session_state.p2pserver.wallet.get_public_key()
    private_key = st.session_state.p2pserver.wallet.get_private_key()
    balance = st.session_state.blockchain.get_balance(
        public_key
    )
    stake = st.session_state.blockchain.get_stake(public_key)
    
    #DISPLAY THE DETAILS
    st.write("Current Balance = ", balance)
    if st.session_state.validator:
        st.write("Currrent Stake in Network = ", stake)
    st.write("Current Reputation = ", balance + stake)
    
    with st.expander("Click to view private key"):
        st.write(private_key)
        
    with st.expander("Click to view private key"):
        st.write(private_key)

    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
