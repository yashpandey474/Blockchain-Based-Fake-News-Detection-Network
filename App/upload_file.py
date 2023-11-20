import streamlit as st
from pyblock.wallet.transaction import *
import change_screen as change_screen_


def upload_file():

    navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
    selected_option = st.sidebar.radio("Navigation", navigation_options)
    if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
        change_screen_.change_screen_navbar(selected_option)
        
    if st.session_state.screen == "upload_file":
        st.markdown(
            "<h1 style='text-align: center;'>Upload New News to the network</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
    """
    ## Upload News Guidelines
    
    As an anonymous user or an auditor of the network, you have the privilege to upload news to the network. 
    Please ensure the following when uploading news:
    
    - **File Format:** Upload a text file (.txt) containing the news article or information.
    
    - **Transaction Fee:** Optionally, you can include a transaction fee to prioritize your news on the network. 
      Ensure the fee is within your available balance.
    
    - **Authentication:** Anonymous uploaders must abide by network guidelines and refrain from uploading fake news as this would lead to reputation penalties.
    
    By contributing news, you help maintain a diverse and informative network for all users.
    """
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
        # if st.button("Back"):
        #     # Set the previous screen in the session state
        #     with st.spinner("Please Wait"): 
        #         change_screen_.change_screen("main_page")
