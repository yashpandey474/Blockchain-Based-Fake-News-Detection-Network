# from your_module import Block, config  # Import necessary modules
import streamlit as st
import change_screen as change_screen_
import pyblock.config as config
from pyblock.blockchain.block import *
import time
from pyblock.wallet.transaction import *
from datetime import datetime
def block_valid():
    return int(time.time()) - st.session_state.p2pserver.received_block.timestamp <= config.BLOCK_VALIDATOR_CHOOSE_INTERVAL

#CREATE A NEW BLOCK
def propose_block():
    if st.session_state.screen == "propose_block":
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            """
            <style>
            .stRadio p{
                font-size: 20px;
            }
            .stRadio>label>div>p{
                font-size: 24px;
            }
            </style>
            """, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen and change_screen_.screen_mapping[selected_option] != "view_block_status":
            change_screen_.change_screen_navbar(selected_option)
            
        st.markdown(
            "<h1 style='text-align: center;'>You are the current block proposer</h1>",
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            ## Block Proposer Responsibilities
            
            As the block proposer in our trusted network, your role is crucial:
            
            - **Transaction Selection:** Choose credible transactions relevant to the network. 
            
            - **News Voting:** Ensure fair and accurate voting on news credibility.
            
            - **Block Creation:** Once satisfied, create and broadcast the block to the network.
            
            Remember, your actions shape the integrity of the network's information.
            """
        )
        
        if st.session_state.p2pserver.received_block:
            st.write("You have already transmitted the block")
            st.write("Current Confirmations on Block: ", len(
                st.session_state.p2pserver.received_block.votes))
        
        else:
            #TABLE DATA TO SHOW TRANSACTIONS
            selected_transactions = []
            votes = {}
            public_key = st.session_state.p2pserver.wallet.get_public_key()
            
            #GET CURRENT MEMPOOL TRANSACTIONS
            transactions = st.session_state.p2pserver.transaction_pool.transactions

            if not transactions:
                st.warning("No transactions in the mempool.")
                
            else:
                #FOR EACH TRANSACTION
                for transaction in transactions:
                    st.subheader(f"Transaction {transaction.id}")
                    
                    #SHOW IMPORTANT DATA RELATED TO TRANSACTION
                    st.markdown(
                        f"""<span><b>Model Fake Score: {transaction.model_score},<br>
                            Transaction Creation Time: {datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y")},<br>
                            Sender Reputation: {transaction.sender_reputation}</b></span>"""       , unsafe_allow_html=True)

                    #WHETHER TO INCLUDE IN BLOCK OR NOT
                    include_value = st.radio("Include Transaction in Block?", [
                                            "False", "True"], key=f"include_{transaction.id}")
                    
                    #WHETHER NEWS IS FAKE OR TRUE
                    vote_value = st.radio("Vote on News:", [
                                        "Fake", "True"], key=f"vote_{transaction.id}")
                    
                    if include_value == "True":
                        selected_transactions.append(transaction)
                        votes[transaction.id] = vote_value


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
                    with st.spinner("Please Wait.."):
                        st.session_state.p2pserver.broadcast_block(block)

                    # CONFIRMATION MESSAGE
                    st.success("The created block was transmitted.")
                    
                    
                    st.session_state.created_block = True
                    st.rerun()

    
def view_block_status():
    #RADIO BUTTONS FOR SIDEBAR
    navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
    st.markdown(
            """
            <style>
            .stRadio p{
                font-size: 20px;
            }
            .stRadio>label>div>p{
                font-size: 24px;
            }
            </style>
            """, unsafe_allow_html=True)
    selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
    if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
        change_screen_.change_screen_navbar(selected_option)
              
    
    if st.session_state.screen == "view_block_status":        
        st.title("View Current Block Status")
        
        if st.session_state.p2pserver.block_proposer == st.session_state.wallet.get_public_key():
            with st.spinner("Please Wait"):
                change_screen_.change_screen("propose_block")

        
        if st.session_state.p2pserver.received_block and block_valid() and st.session_state.validator:
            st.write("A valid block has been received.")
            if st.button("Vote on Received Block"):
                with st.spinner("Please Wait"): 
                    change_screen_.change_screen("vote_on_block")

            
        st.write("Current Block Proposer Public Key: ", st.session_state.p2pserver.block_proposer)
        if st.session_state.p2pserver.received_block:
            st.write("Current Confirmations on Receieved Block: ", len(st.session_state.p2pserver.received_block.votes))
        else:
            st.write("No Valid Block Received yet.")
            

                
        
