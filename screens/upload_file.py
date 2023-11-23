import streamlit as st
from wallet.transaction import Transaction
import change_screen as change_screen_
import time 
def upload_file():

    navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
    st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
    selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
    if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
        change_screen_.change_screen_navbar(selected_option)
        
    if st.session_state.screen == "upload_file":
        st.markdown(
            change_screen_.upload_file_message
        )
        if not st.session_state.get("upload_file_executed", False):
            uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
            
            if uploaded_file is not None:
                balance = st.session_state.blockchain.get_balance(
                    st.session_state.p2pserver.wallet.get_public_key()
                )
                st.write("Your current balance: ", balance)
                
                # ASK FOR OPTIONAL TRANSACTION FEE
                transaction_fee = st.number_input(
                    "Enter transaction fee amount you want to include", 
                    min_value = 0,
                    max_value = int(balance),
                    step = 1
                )
                
                if st.button("Submit News"):

                    
                    # BROADCASE NEWLY CREATED TRANSACTION
                    with st.spinner("Running Machine Learning Model.."):
                        st.session_state.transaction_fee = transaction_fee
                        transaction = Transaction.generate_from_file(
                            sender_wallet=st.session_state.p2pserver.wallet,
                            file=uploaded_file,
                            blockchain=st.session_state.p2pserver.blockchain,
                            fee = st.session_state.transaction_fee
                        )

                    with st.spinner("Broadcasting Transation.."):
                        st.session_state.p2pserver.broadcast_transaction(
                            transaction
                        )
                        
                        st.session_state.upload_file_executed = True
                        
                    print("BROADCASTED TRANSACTION")
                    st.success("File successfully uploaded.")
                    
        else:
            st.success("File successfully uploaded.")