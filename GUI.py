# from flask import Flask, request, jsonify, redirect
from pyblock.wallet.transaction import PartialTransaction, Transaction
import streamlit as st
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
import pyblock.config as config
import threading


blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()
p2pserver = P2pServer(blockchain, transaction_pool, wallet)

#START LISTENING ON P2P SERVER
def run_p2pserver():
    print("Running p2p server on port: "+str(config.P2P_PORT))
    p2pserver.listen()


#SHOW ALL ACCOUNT RELATED INFO
def show_account_info():
    st.title("ACCOUNT INFORMATION")
    balance = wallet.get_balance()
    public_key = wallet.get_public_key()
    st.write("BALANCE = ", balance)
    st.write("PUBLIC KEY = ", public_key)
    
#SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
def show_transactions():
    st.title("Current Network Transactions")
    table_data = []
    for transaction in transaction_pool.transactions:
        table_data.append({
            "ID": transaction.partialTransaction.id,
            "IPFS Address": transaction.partialTransaction.ipfs_address,
            "Sender Address": transaction.partialTransaction.sender_address,
            "Validator Address": transaction.validator_address,
            "Sign": transaction.sign,
            "Votes": transaction.votes,
            "Timestamp": transaction.timestamp,
            "Model Score": transaction.model_score
        })

    st.table(table_data)
    
    
#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
def show_blocks_news():
    pass


#STREAMLIT GUI
def main_page():
    st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, user.")
        
    if st.button("Upload New News"):
            #GET UPLOADED TEXT FILE
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

            #CREATE PARTIAL TRANSACTION
        partial_transaction = PartialTransaction.generate_from_file(uploaded_file)
            
            #CREATE TRANSACTION
        transaction = Transaction.create_transaction(partial_transaction, wallet)
        
        #BROADCASE NEWLY CREATED TRANSACTION
        p2pserver.broadcast_transaction(transaction)
            
            
    if st.button("View all Verified News"):
        # contest_validation()
        show_blocks_news()
            
    if st.button("View Account Information"):
        show_account_info()
        
    if st.button("View all transactions in mempool"):
        show_transactions()
            
        
if __name__ == '__main__':
    p2p_thread = threading.Thread(target=run_p2pserver)
    p2p_thread.start()
    main_page()
