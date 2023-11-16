# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
from datetime import datetime
import streamlit as st
from .qr_handler import make_qr

def show_transaction(transaction):

    data = f"""
        Model Score: {transaction.model_score}\n
        Sender Reputation: {transaction.sender_reputation}\n
        Sender Stake: {st.session_state.p2pserver.blockchain.get_stake(transaction.sender_address)}\n
        Transaction Fee: {transaction.fee}\n
        Timestamp: {datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y")}\n
        Sender Address: {transaction.sender_address}\n
        ID: {transaction.id}\n
        Content URL: https://{transaction.ipfs_address}.ipfs.dweb.link
    """

    return make_qr(data)
