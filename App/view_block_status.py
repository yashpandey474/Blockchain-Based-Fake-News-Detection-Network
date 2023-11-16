# from your_module import Block, config  # Import necessary modules
import streamlit as st
from change_screen import *
import pyblock.config as config
from pyblock.blockchain.block import *
import time

def block_valid():
    return int(time.time()) - st.session_state.p2pserver.received_block.timestamp <= config.BLOCK_VALIDATOR_CHOOSE_INTERVAL

#CREATE A NEW BLOCK
def propose_block():
    st.title("You are the current block proposer.")

    if "created_block" in st.session_state and st.session_state.created_block == True:
        st.write("You have already transmitted the block")
        st.write("Current Confirmations on Block: ", len(
            st.session_state.p2pserver.received_block.votes))
    
    else:
        #TABLE DATA TO SHOW TRANSACTIONS
        table_data = []
        selected_transactions = []
        votes = {}
        public_key = st.session_state.p2pserver.wallet.get_public_key()
        
        #GET CURRENT MEMPOOL TRANSACTIONS
        transactions = st.session_state.p2pserver.transaction_pool.transactions

<<<<<<< HEAD
        if not transactions:
            st.warning("No transactions in the mempool.")
        else:
            #FOR EACH TRANSACTION
            for transaction in transactions:
                st.subheader(f"Transaction {transaction.id}")
                
                #WHETHER TO INCLUDE IN BLOCK OR NOT
                include_value = st.radio("Include in Block?", [
                                        "False", "True"], key=f"include_{transaction.id}")
                
                #WHETHER NEWS IS FAKE OR TRUE
                vote_value = st.radio("Vote on this Transaction?", [
                                    "False", "True"], key=f"vote_{transaction.id}")
                
                if include_value == "True":
                    selected_transactions.append(transaction)
                    votes[transaction.id] = vote_value
=======

        #FOR EACH TRANSACTION
        for transaction in transactions:
            st.subheader(f"Transaction {transaction.id}")
            
            #WHETHER TO INCLUDE IN BLOCK OR NOT
            include_value = st.radio("Include in Block?", [
                                    "False", "True"], key=f"include_{transaction.id}")
            
            #WHETHER NEWS IS FAKE OR TRUE
            vote_value = st.radio("Vote on this Transaction?", [
                                "False", "True"], key=f"vote_{transaction.id}")
            
            if include_value == "True":
                selected_transactions.append(transaction)
                votes[transaction.id] = vote_value
>>>>>>> 84563e1 (Fix votes)


            # WARN USER IF MORE THAN ALLOWED TRANSACTIONS SELECTED
            print(selected_transactions)
            print(len(selected_transactions))
            max_selections = config.BLOCK_TRANSACTION_LIMIT
            
            if len(selected_transactions) > max_selections:
                st.warning(
                    f"Maximum selections allowed: {max_selections}. Please deselect items.")

            # CONFIRM THE SELECTION AND VOTES
            if st.button("Create Block") and 1 <= len(selected_transactions) <= max_selections:
                print("BLOCK BEING CREATED")
                for transaction in selected_transactions:
                    if votes[transaction.id] == "True":
                        transaction.positive_votes.add(public_key)
                    else:
                        transaction.negative_votes.add(
                            public_key)
                
                # CREATE A BLOCK WITH TRANSACTIONS (PASSED AS LIST)
                block = Block.create_block(
                    lastBlock=st.session_state.blockchain.chain[-1],
                    data=selected_transactions,
                    wallet=st.session_state.p2pserver.wallet,
                    blockchain=st.session_state.p2pserver.blockchain
                )
                
                print(block.transactions)
                
                #ADD THE ADDRESS TO VOTE
                block.votes.add(st.session_state.wallet.get_public_key())

                # BROADCAST THE BLOCK
                st.session_state.p2pserver.broadcast_block(block)

<<<<<<< HEAD
                # CONFIRMATION MESSAGE
                st.success("The created block was transmitted.")
                
                
                # st.session_state.created_block = True
                # st.rerun()
=======
            # CONFIRMATION MESSAGE
            st.success("The created block was transmitted.")
            
            
            st.session_state.created_block = True
            st.rerun()
>>>>>>> 84563e1 (Fix votes)

    if st.button("Back"):
        change_screen("main_page")

    
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
        
    if st.button("Back"):
        change_screen("main_page")
            
    
