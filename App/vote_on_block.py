import streamlit as st
from change_screen import *

def vote_on_block():
    st.title("Vote on Recieved Block News.")
    
    if st.session_state.voted:
        st.write("You have already voted on the current proposed block.")
        
    else:
        st.header("Block Info")
        st.write("Validator:", block.validator)
        st.write("Timestamp:", block.timestamp)
        
        
        block = st.session_state.recieved_block
        transaction_votes = {}
        table_data = []

        for transaction in block.data:
            transaction_id = transaction.id
            vote = st.radio(
                    f"Vote for Transaction {transaction_id}", ("True", "False"))
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

