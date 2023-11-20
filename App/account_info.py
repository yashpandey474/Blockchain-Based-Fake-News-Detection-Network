from pyblock.wallet.transaction import *
import streamlit as st
import change_screen as change_screen_


def show_account_info():
    if st.session_state.screen == "account_info":
        # nav_selection = st.sidebar.selectbox("Navigation", change_screen_.navigation_options.get(st.session_state.user_type, ()))
        # if nav_selection and change_screen_.screen_mapping[nav_selection] != st.session_state.screen:
        #     change_screen_.change_screen_navbar(nav_selection)
        
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
            "<h1 style='text-align: center;'>ACCOUNT INFORMATION</h1>",
            unsafe_allow_html=True
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
            st.write(private_key)
            
        with st.expander("Click to view public key"):
            st.write(public_key)

        # if st.button("Back"):
        #     with st.spinner("Please Wait"): 
        #         change_screen_.change_screen(st.session_state.previous_screen)
