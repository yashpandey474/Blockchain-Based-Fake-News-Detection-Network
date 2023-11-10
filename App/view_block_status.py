import streamlit as st
from change_screen import *
import pyblock.config as config
from pyblock.blockchain.block import *
import time

def block_valid():
    return int(time.time()) - st.session_state.p2pserver.received_block.timestamp <= config.BLOCK_VALIDATOR_CHOOSE_INTERVAL

def propose_block():
    st.title("Create A Block")
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
                data=selected_transaction_objects,
                wallet=st.session_state.p2pserver.wallet,
                blockchain=st.session_state.p2pserver.blockchain
            )
        

            # BROADCAST THE BLOCK
        st.session_state.p2pserver.broadcast_block(block)

            # CONFIRMATION MESSAGE
        st.write("The created block was transmitted.")
    
    
def view_block_status():

    # IF USER IS THE CURRENT BLOCK PROPOSER
    if st.session_state.p2pserver.block_proposer == st.session_state.wallet.get_public_key():
       change_screen("propose_block")
       
    st.title("View Current Block Status")

    if st.session_state.p2pserver.received_block and block_valid():
        st.write("A valid block has been received.")
        if st.button("Vote on Received Block"):
            change_screen("vote_on_block")
        
    st.write("Current Block Proposer Public Key: ", st.session_state.p2pserver.block_proposer)
    if st.session_state.p2pserver.received_block:
        st.write("Current Confirmations on Receieved Block: ", len(st.session_state.p2pserver.received_block.votes))
    else:
        st.write("No Valid Block Received yet.")
            
    
