import streamlit as st
import change_screen

def vote_on_block():
    if st.session_state.screen == "vote_on_block":
        nav_selection = st.sidebar.selectbox("Navigation", change_screen.navigation_options.get(st.session_state.user_type, ()))
        if nav_selection and change_screen.screen_mapping[nav_selection] != st.session_state.screen:
            change_screen.change_screen_navbar(nav_selection)
            
        # st.title("Vote on Recieved Block News.")
        st.markdown(
            "<h1 style='text-align: center;'>Vote on Received Block</h1>",
            unsafe_allow_html=True
        )    # IF RECEIVED A BLOCK
            
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
                        f"Vote on News", ("True", "Fake")
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
                    with st.spinner("Please Wait.."):
                        st.session_state.p2pserver.broadcast_votes(
                            transaction_votes
                        )

                    st.write("Votes Submitted. Thank you")

                    st.session_state.voted = True
                    
        if st.button("Back"):
            # Set the previous screen in the session state
            with st.spinner("Please Wait"):
                change_screen.change_screen(st.session_state.previous_screen)

