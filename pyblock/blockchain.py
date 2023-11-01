import streamlit as st
from wallet.transaction import *
from wallet.wallet import *

#INITIALISE WALLET
wallet = Wallet()
def show_blockchain():
    st.title("FAKE NEWS DETECTION BLOCKCHAIN")
    st.write("Welcome to the blockchain system for fake news detection.")
    
    if st.button("Upload New News"):
        #GET UPLOADED TEXT FILE
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

        #CREATE PARTIAL TRANSACTION
        partial_transaction = PartialTransaction.generate_from_file(uploaded_file)
        
        #CREATE TRANSACTION
        transaction = Transaction.create_transaction(partial_transaction, wallet)
        
        
        
    if st.button("Contest for validation"):
        contest_validation()
        
    if st.button("View Account Information"):
        show_account_info()
        
        