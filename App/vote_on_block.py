import streamlit as st
import change_screen as change_screen_

def vote_on_block():
    if st.session_state.screen == "vote_on_block":

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
    """
    # Vote on Received Block

    This section allows you to vote on the block proposed within the network.

    ## Block Information:

    Here are the details of the proposed block:

    - **Validator:** [Validator's Public Key]
    - **Timestamp:** [Timestamp of Block]
    - **Validator Reputation:** [Validator's Reputation]

    ## Transactions in Block:

    Below, you'll find the transactions included in the proposed block along with their details:

    """
)

        if not st.session_state.p2pserver.received_block:
            st.write("No valid block received yet.")
            
        if st.session_state.p2psever.voted:
            st.write("You have already voted on the current proposed block.")
            
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
                        f"Vote on News", ("True", "Fake")
                )
                
                transaction_votes[transaction_id] = vote
                
                table_data.append({
                        "ID": transaction.id,
                        "IPFS Address": transaction.ipfs_address,
                        "Sender Address": transaction.sender_address,
                        "Sender Reputation": transaction.sender_reputation,
                        "Model Score": transaction.model_score,
                        "Vote": vote,
                    })

            st.table(table_data)

            st.markdown(
    """
    Please review the transactions and provide your vote for each transaction as either "True" or "Fake".
    Once you've made your selections, click the "Submit Votes" button to cast your votes. 
    Thank you for your participation!
    """
)
                
            if st.button("Submit Votes"):
                with st.spinner("Please Wait.."):
                    st.session_state.p2pserver.broadcast_votes(
                            transaction_votes
                        )

                st.write("Votes Submitted. Thank you")

                st.session_state.p2pserver.voted = True
                    
