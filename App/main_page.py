# STREAMLIT GUI
import streamlit as st
from change_screen import *
from pyblock.wallet.transaction import *
from pyblock import config
from pyblock.blockchain.block import *
import time

def main_page():
    # st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, " + st.session_state.name)

    if st.button("Upload New News"):
        # GET UPLOADED TEXT FILE
        change_screen("upload_file")

    # VIEW NEWS STORED IN BLOCKCHAIN
    if st.button("View all Verified News"):
        change_screen("show_blocks")

    if st.button("View Account Information"):
        change_screen("account_info")

    if st.session_state.user_type == "Auditor":
        if st.button("View all transactions in mempool"):
            change_screen("show_transac")

        if st.button("Become a Validator."):
            change_screen("become_validator")
            

    # IF THE USER IS A VALIDATOR AND CURRENT BLOCK PROPOSER
    if st.session_state.validator and st.session_state.block_proposer == st.session_state.wallet.public_key:
        st.write("You are the current block proposer.")
        # SHOW TRANSACTION POOL AND ASK TO CHOOOSE TRANSACTIONS
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

        # DISPLAY TABLE OF TRANSACS. WITH SELECT BOX
        selected_transactions = st.multiselect(
            "Select transactions to Include in Block ",
            table_data,
            default=[],
            key="transactions",
        )

        # WARN USER IF MORE THAN ALLOWED TRANSACTIONS SELECTED
        if len(selected_transactions) > max_selections:
            st.warning(
                f"Maximum selections allowed: {max_selections}. Please deselect items."
            )

        # CONFIRM THE SELECTION
        if st.button("Confirm Selection") and len(selected_transactions) <= max_selections:
            selected_transaction_objects = [
                transaction_dict[transaction["ID"]] for transaction in selected_transactions
            ]

            # CREATE A BLOCK WITH TRANSACTIONS [PASSED AS LIST]
            block = Block.create_block(
                lastBlock=st.session_state.blockchain.chain[-1],
                _data=selected_transaction_objects,
                wallet=st.session_state.p2pserver.wallet,
                blockchain=st.session_state.p2pserver.blockchain
            )

            # BROADCAST THE BLOCK
            st.session_state.p2pserver.broadcast_block(block)

            # CONFIRMATION MESSAGE
            st.write("The created block was transmitted. Waiting for confirmations.")

    if st.session_state.validator:
        
        # IF RECEIVED A BLOCK
        if st.session_state.block_recieved and st.button("Vote on Recieved Block"):
            # SHOW THE BLOCK'S TRANSACTIONS AND ASK FOR VOTES
            change_screen("vote_on_block")
        
        st.write("Current Block Proposer: ", st.session_state.block_proposer)

        if st.session_state.recieved_block is not None:
            st.write("Current Confirmations on Block: ", st.session_state.recieved_block.votes)
        
    # GO TO PREVIOUS SCREEN
    if st.button("Go to Enter Page"):
            # Set the previous screen in the session state
        change_screen("enter")
        
    # TODO: FIX EXITING
    if st.button("Exit Application."):
        st.stop()

    