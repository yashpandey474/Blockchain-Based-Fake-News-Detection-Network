# from flask import Flask, request, jsonify, redirect
from pyblock.wallet.transaction import PartialTransaction, Transaction
import streamlit as st
import crypto_logic
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
import pyblock.config as config
import threading
from pyblock.blockchain.account import *
from pyblock.blockchain.stake import *


#START LISTENING ON P2P SERVER
def run_p2pserver(p2pserver):
    print("Running p2p server on port: "+str(config.P2P_PORT))
    p2pserver.listen()
    
#INSTANTIATE  VARIABLES NEEDED BETWEEN RERUNS OF STREAMLIT APP


    
    

#SHOW ALL ACCOUNT RELATED INFO
def show_account_info(wallet, blockchain):
    st.title("ACCOUNT INFORMATION")
    balance = blockchain.get_balance(wallet.public_key)
    public_key = wallet.get_public_key()
    st.write("BALANCE = ", balance)
    st.write("PUBLIC KEY = ", public_key)
    
#SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
def show_transactions(transaction_pool):
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

#CHANGE THE SCREEN OF GUI
def change_screen(input_string):
    st.session_state.screen = input_string
    st.experimental_rerun()
    
#STREAMLIT GUI
def main_page(p2pserver, wallet):
    st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, user.")
        
    if st.button("Upload New News"):
            #GET UPLOADED TEXT FILE
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

        if uploaded_file:
                #CREATE PARTIAL TRANSACTION
            partial_transaction = PartialTransaction.generate_from_file(sender_wallet = wallet, file = uploaded_file)
                
                #CREATE TRANSACTION
            transaction = Transaction.create_transaction(partial_transaction, wallet)
            
            #BROADCASE NEWLY CREATED TRANSACTION
            p2pserver.broadcast_transaction(transaction)
                
            
    if st.button("View all Verified News"):
        change_screen("show_blocks")
            
    if st.button("View Account Information"):
        change_screen("account_info")
        
    if st.button("View all transactions in mempool"):
        change_screen("show_transac")


def login():
    st.title("Login")
    user_input = st.text_input("Enter your Private Key")
    if user_input:
        vc = crypto_logic.verify(user_input)
        if vc[0]:
            change_screen("main_page")
            
        else:
            st.write(vc[1])

    if st.button("Sign up"):
        change_screen("sign_up")

def sign_up():
    st.title("Sign Up")
    
    if st.button("Gen new key"):
        st.write("new key, wont see again, keep for future")
        st.write(crypto_logic.gen_sk())
        st.session_state.gen_key_pressed = True

    if st.session_state.gen_key_pressed:
        if st.button("Go to main"):
            print("BUTTON CLICKED")
            change_screen("main_page")
            



def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen == "login":
        print("CALL: LOGIN")
        login()
            
    if st.session_state.screen == "main_page":
        print("YES. WE TRIED TO CALL THE MAIN PAGE")
        main_page(st.session_state.p2pserver, st.session_state.wallet)
            
    if st.session_state.screen == "account_info":
        print("CALL: ACC INFO")
        show_account_info(wallet= st.session_state.wallet, blockchain= st.session_state.blockchain)
        
    if st.session_state.screen == "show_transac":
        print("CALL: SHOW TRANSAC")
        show_transactions(transaction_pool = st.session_state.transaction_pool)
            
    if st.session_state.screen == "show_blocks":
        print("CALL: SHOW BLOCKS")
        show_blocks_news()

    if st.session_state.screen == "sign_up":
        sign_up()


if __name__ == "__main__":
    if "blockchain" not in st.session_state:
        st.session_state.blockchain = Blockchain()

    if "wallet" not in st.session_state:
        st.session_state.wallet = Wallet()

    if "accounts" not in st.session_state:
        st.session_state.accounts = Account()

    if "transaction_pool" not in st.session_state:
        st.session_state.transaction_pool = TransactionPool()

    if "stake" not in st.session_state:
        st.session_state.stake = Stake()

    if "p2pserver" not in st.session_state:
        print("P2P SERVER CALLED!")
        st.session_state.p2pserver = P2pServer(
            blockchain=st.session_state.blockchain, transaction_pool=st.session_state.transaction_pool,
            stakes=st.session_state.stake, wallet=st.session_state.wallet, account=st.session_state.accounts
        )
        p2p_thread = threading.Thread(
            target=run_p2pserver, args=(st.session_state.p2pserver,))
        p2p_thread.start()
        
    if "screen" not in st.session_state:
        print("SCREEN INITILIASED")
        st.session_state.screen = "login"
        
    if "gen_key_pressed" not in st.session_state:
        st.session_state.gen_key_pressed = False
        
    main()