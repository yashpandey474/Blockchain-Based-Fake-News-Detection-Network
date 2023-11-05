# from flask import Flask, request, jsonify, redirect
from pyblock.wallet.transaction import PartialTransaction, Transaction
import streamlit as st
import pandas as pd
import crypto_logic
from pyblock.blockchain.blockchain import Blockchain
from pyblock.blockchain.block import *
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
import pyblock.config as config
import threading
from pyblock.blockchain.account import *
import time

# https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmxvY2tjaGFpbnxlbnwwfHwwfHx8MA%3D%3D
# https://i.pinimg.com/originals/88/15/63/881563d6444b370fa4ceea0c3183bb4c.gif

background_style = '''<style>
section {
background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmxvY2tjaGFpbnxlbnwwfHwwfHx8MA%3D%3D");
background-size: cover;
background-position: center;
transition: transform 0.3s ease-in-out;
width: 100%;
height: 100vh;
}
</style>
<script>
        const sections = document.querySelectorAll("section");
    sections.forEach(section => {
        section.addEventListener("mousemove", function(e) {
            const width = section.offsetWidth;
            const height = section.offsetHeight;
            const offsetX = 0.5 - e.pageX / width;
            const offsetY = 0.5 - e.pageY / height;
            section.style.transform = "perspective(1000px) rotateX(" + (offsetY * 4) + "deg) rotateY(" + (offsetX * 4) + "deg)";
        });
        section.addEventListener("mouseleave", function() {
            this.style.transform = "none";
        });
    });
    </script>
'''

st.markdown(background_style, unsafe_allow_html=True)


# st.markdown(
#     """
#     <iframe
#       src="HTML/custom_background.html"
#       width="100%"
#       height="100%"
#     >
#     </iframe>
#     """,
#     unsafe_allow_html=True,
# )
st.title("Fake News Detection System Utilising Blockchain")



#START LISTENING ON P2P SERVER
def run_p2pserver(p2pserver):
    print("Running p2p server on port: "+str(config.P2P_PORT))
    p2pserver.listen()
    
#INSTANTIATE  VARIABLES NEEDED BETWEEN RERUNS OF STREAMLIT APP


    
    

#SHOW ALL ACCOUNT RELATED INFO
def show_account_info():
    st.title("ACCOUNT INFORMATION")
    balance = st.session_state.blockchain.get_balance(st.session_state.wallet.public_key)
    public_key = st.session_state.wallet.get_public_key()
    st.write("BALANCE = ", balance)
    st.write("PUBLIC KEY = ", public_key)
    
#SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
def show_transactions(transaction_pool):
    st.title("Current Network Transactions")
    
    table_data = []
    for transaction in transaction_pool.transactions:
        table_data.append({
            "ID": transaction.id,
            "Timestamp": transaction.timestamp,
            "IPFS Address": transaction.ipfs_address,
            "Sender Address": transaction.sender_address,
            "Sender Reputation": transaction.validator_address,
            "Sign": transaction.sign,
            "Model Score": transaction.model_score
        })

    st.dataframe(pd.DataFrame(table_data), height=500)
    
    
#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
def show_blocks_news():
    chain = st.session_state.p2pserver.blockchain.chain
    
    table_data = []
    
    for block in chain:
        for transaction in block.data:
            table_data.append({
                "ID": transaction.id,
                "Transaction Creation Time": transaction.timestamp,
                "Block Creation Time": block.timestamp,
                "IPFS Address": transaction.ipfs_address,
                "Sender Address": transaction.sender_address,
                "Validator Address": block.validator,
                "Sender Reputation": transaction.sender_reputation,
                "Sign of sender": transaction.sign,
                "Model Score": transaction.model_score
            })
            
    st.dataframe(pd.DataFrame(table_data), height=500)

#CHANGE THE SCREEN OF GUI
def change_screen(input_string):
    st.session_state.screen = input_string
    st.rerun()
    
#STREAMLIT GUI
def main_page():
    # st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, user.")
        
    if st.button("Upload New News"):
            #GET UPLOADED TEXT FILE
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

        if uploaded_file:
            #CREATE PARTIAL TRANSACTION
            partial_transaction = Transaction.generate_from_file(sender_wallet = st.session_state.p2pserver.wallet, file = uploaded_file)
            
            #BROADCASE NEWLY CREATED TRANSACTION
            st.session_state.p2pserver.broadcast_transaction(partial_transaction)
                
    #VIEW NEWS STORED IN BLOCKCHAIN
    if st.button("View all Verified News"):
        change_screen("show_blocks")
        
    if st.button("View Account Information"):
        change_screen("account_info")

    if st.session_state.user_type == "Auditor":
        if st.button("View all transactions in mempool"):
            change_screen("show_transac")
            
        
        if st.button("Become a Validator."):

            if st.session_state.validator:
                st.write("You are already a validator.")
                
            else:
                current_balance = st.session_state.accounts.get_balance(st.session_state.wallet.public_key)
                
                if current_balance < config.MIN_STAKE:
                    st.write("You don't have enough balance to stake.")
                    
                else:
                    st.session_state.try_be_validator = True
            
        if st.session_state.try_be_validator:
            st.write("Please enter an amount to stake.")
            st.write("Minimum Stake Required: ", config.MIN_STAKE)
            st.write("Your Current Balance: ", current_balance)
            st.session_state.numerical_value = st.number_input("Enter a numerical value", min_value = config.MIN_STAKE, max_value = current_balance, value=config.MIN_STAKE, step=1)
            
            if st.button("Submit Stake"):
                st.session_state.p2pserver.broadcast_new_validator(stake = st.session_state.numerical_value)
                st.write("You are successfully registered as a validator.")
                st.session_state.validator = True
                
                time.sleep(1)
                st.session_state.try_be_validator = False
                
    
    #IF THE USER IS A VALIDATOR AND CURRENT BLOCK PROPOSER
    if st.session_state.validator and st.session_state.block_proposer == st.session_state.wallet.public_key:
        #SHOW TRANSACTION POOL AND ASK TO CHOOOSE TRANSACTIONS
        table_data = []
        transactions = st.session_state.p2pserver.transaction_pool.transactions
        transaction_dict = {
            transaction.id: transaction for transaction in transactions
            }

        for transaction in transactions:
            table_data.append({
                "ID": transaction.id,
                "IPFS Address": transaction.ipfs_address,
                "Model Score": transaction.model_score,
                "Sender Reputation": transaction.sender_reputation
            })

        max_selections = config.BLOCK_TRANSACTION_LIMIT
        
        #DISPLAY TABLE OF TRANSACS. WITH SELECT BOX
        selected_transactions = st.multiselect(
            "Select transactions",
            table_data,
            default=[],
            key="transactions",
        )

        #WARN USER IF MORE THAN ALLOWED TRANSACTIONS SELECTED
        if len(selected_transactions) > max_selections:
            st.warning(
                f"Maximum selections allowed: {max_selections}. Please deselect items."
                )

        #CONFIRM THE SELECTION
        if st.button("Confirm Selection") and len(selected_transactions) <= max_selections:
            selected_transaction_objects = [
                transaction_dict[transaction["ID"]] for transaction in selected_transactions
            ]

            #CREATE A BLOCK WITH TRANSACTIONS [PASSED AS LIST]
            block = Block.create_block(
                lastBlock = st.session_state.blockchain.chain[-1],
                _data = selected_transaction_objects,
                wallet = st.session_state.p2pserver.wallet
            )
            
            #BROADCAST THE BLOCK
            st.session_state.p2pserver.broadcast_block(block)
            
            #CONFIRMATION MESSAGE
            st.write("The created block was transmitted. Waiting for confirmations.")
            

            st.session_state.block_confirmations = 0
    
    elif st.session_state.validator:
        st.write("Current Block Proposer: ", st.session_state.block_proposer)
            
    if "block_confirmations" in st.session_state and st.session_state.block_confirmations >= 0:
        st.write("Current Confirmations: ", st.session_state.block_confirmations)
        
        
                
def initialise(private_key = None):
    if "blockchain" not in st.session_state:
        st.session_state.blockchain = Blockchain()

        st.session_state.accounts = st.session_state.blockchain.accounts

        st.session_state.transaction_pool = TransactionPool()

        st.session_state.wallet = Wallet(private_key)
        
        print("P2P SERVER CALLED!")
        
        st.session_state.p2pserver = P2pServer(
            blockchain=st.session_state.blockchain, transaction_pool=st.session_state.transaction_pool, wallet=st.session_state.wallet, accounts=st.session_state.accounts
        )
        
        p2p_thread = threading.Thread(
            target=run_p2pserver, args=(st.session_state.p2pserver,)
        )
        
        p2p_thread.start()
        
        print("EVERYTHING INITIIALISED")


def login():
    st.title("Login")

    user_input = st.text_area("Enter your Private Key")

    if st.button("Continue"):
        
        if user_input:
            vc = crypto_logic.verify(user_input)
            
            if vc[0]:
                initialise(vc[2])
                change_screen("main_page")
                
            else:
                st.write(vc[1])

    if st.button("Sign up"):
        change_screen("sign_up")

def sign_up():
    st.title("Sign Up")
    
    if st.button("Gen new key"):
        st.write("new key, wont see again, keep for future")
        
        private_key = crypto_logic.gen_sk()
        
        st.session_state.initialise = True
        
        initialise(private_key)
        
        st.write(private_key.export_key().decode())
        
        st.session_state.gen_key_pressed = True

    if st.session_state.gen_key_pressed:
        if st.button("Go to main"):
            print("BUTTON CLICKED")
            change_screen("main_page")
            

def enter():
    st.title("Choose Role to enter into Network")
    
    if st.button("Login/Signup as News Auditor"):
        st.session_state.user_type = "Auditor"
        print("BUTTON CLICKED")
        change_screen("login")
    
    if st.button("Enter as a Reader."):
        st.session_state.user_type = "Reader"
        
        print("BUTTON CLICKED")
        initialise()
        
        change_screen("main_page")

def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen == "enter":
        print("CALL: ENTER")
        enter()
    if st.session_state.screen == "login":
        print("CALL: LOGIN")
        login()
            
    if st.session_state.screen == "main_page":
        print("YES. WE TRIED TO CALL THE MAIN PAGE")
        main_page()
            
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
    if "screen" not in st.session_state:
        
        print("SCREEN INITILIASED")
        st.session_state.initialise = False
        
        st.session_state.screen = "enter"
        
        st.session_state.gen_key_pressed = False
        
        st.session_state.try_be_validator = False

        st.session_state.validator = False
        
    main()
        
