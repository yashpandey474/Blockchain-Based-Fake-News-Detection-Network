import streamlit as st
from change_screen import *

def vote_on_block():
    st.title("Vote on Recieved Block News.")
            # IF RECEIVED A BLOCK 
        
    if st.session_state.voted:
        st.write("You have already voted on the current proposed block.")
        
    if not st.session_state.p2pserver.received_block:
        st.write("No valid block received yet.")
    else:
        block = st.session_state.p2pserver.received_block
        st.header("Block Info")
        st.write("Validator:", block.validator)
        st.write("Timestamp:", block.timestamp)
        st.write("Validator Repuation: ", 
                 st.session_state.p2pserver.blockchain.get_balance(block.validator) + 
                 st.session_state.p2pserver.blockchain.get_stake(block.validator))
        transaction_votes = {}
        table_data = []

        for transaction in block.data:
            transaction_id = transaction.id
            vote = st.radio(
                    f"Vote for Transaction {transaction_id}", ("True", "False")
            )
            
            transaction_votes[transaction_id] = vote

            table_data.append({
                    "ID": transaction.id,
                    "IPFS Address": transaction.ipfs_address,
                    "Sender Address": transaction.sender_address,
                    "Sender Reputation": transaction.sender_reputation,
                    "Model Score": transaction.model_score,
                    "Sign of Sender": transaction.sign,
                    "Vote": vote,
                })

            st.table(table_data)

            if st.button("Submit Votes"):
                st.session_state.p2pserver.broadcast_votes(
                    transaction_votes
                )

                st.write("Votes Submitted. Thank you")

                st.session_state.voted = True
                
    if st.button("Back"):
        # Set the previous screen in the session state
        change_screen(st.session_state.previous_screen)

