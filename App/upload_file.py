import streamlit as st
from pyblock.wallet.transaction import *
from change_screen import *


def upload_file():
    # st.title("Upload New News to the network.")
    if st.session_state.screen == "upload_file":
        st.markdown(
            "<h1 style='text-align: center;'>Upload New News to the network</h1>",
            unsafe_allow_html=True
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

                    transaction = Transaction.generate_from_file(
                        sender_wallet=st.session_state.p2pserver.wallet,
                        file=uploaded_file,
                        blockchain=st.session_state.p2pserver.blockchain,
                        fee=transaction_fee
                    )

                    # st.success(f"Successfully Uploaded File: {uploaded_file.name}")
                    st.session_state.upload_file_executed = True
                    
                    # BROADCASE NEWLY CREATED TRANSACTION
                    with st.spinner("Please Wait.."):
                        st.session_state.p2pserver.broadcast_transaction(
                            transaction
                        )

                    print("BROADCASTED TRANSACTION")
                    st.rerun()
                    
        else:
            st.success("File successfully uploaded.")

        # GO TO PREVIOUS SCREEN
        if st.button("Back"):
            # Set the previous screen in the session state
            with st.spinner("Please Wait"): 
                change_screen("main_page")
