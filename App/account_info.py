from pyblock.wallet.transaction import *
import streamlit as st
import change_screen as change_screen_


def show_account_info():
    if st.session_state.screen == "account_info":
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
            
        st.markdown(
            """
            ## ACCOUNT INFORMATION

            Welcome to the Account Information section.

            Here, you can find details about your account on the network:
            - **Reputation**: Your current reputation calculated as the sum of your balance and stake.
            - **Balance**: The current balance available in your account.
            - **Stake (for Auditors)**: If you're an auditor, this displays your stake in the network.
            - **Private Key**: Click to view your private key (This should be kept confidential).
            - **Public Key**: View your public key for identification in the network.

            Keep your private key secure and never share it with anyone!
            """
        )
        
        #GET USER'S DETAILS
        public_key = st.session_state.p2pserver.wallet.get_public_key()
        private_key = st.session_state.p2pserver.wallet.get_private_key()
        balance = st.session_state.blockchain.get_balance(
            public_key
        )
        stake = st.session_state.blockchain.get_stake(public_key)
        
        #DISPLAY THE DETAILS
        st.write("Current Reputation = ", balance + stake)
        st.write("Current Balance = ", balance)
        if st.session_state.user_type == "Auditor":
            st.write("Currrent Stake in Network = ", stake)
        
        
        with st.expander("Click to view private key"):
            st.markdown(private_key.replace("\n", "<br>"),unsafe_allow_html=True)
            
        with st.expander("Click to view public key"):
            st.markdown(public_key.replace("\n", "<br>"),unsafe_allow_html=True)
