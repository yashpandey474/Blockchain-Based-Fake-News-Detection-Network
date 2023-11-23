import streamlit as st
import change_screen as change_screen_


def show_account_info():
    if st.session_state.screen == "account_info":
        
        #NAVBAR INFO
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
           
        #DISPLAY MESSAGE 
        st.markdown(
            change_screen_.view_account_info_message
        )
        
        #GET USER'S DETAILS
        public_key = st.session_state.p2pserver.wallet.get_public_key()
        private_key = st.session_state.p2pserver.wallet.get_private_key()
        balance = st.session_state.blockchain.get_balance(
            public_key
        )
        stake = st.session_state.blockchain.get_stake(public_key)
        
        #DISPLAY THE DETAILS
        user_type = ("Validating Auditor" if st.session_state.validator else st.session_state.user_type)
        
        st.write("User Type: ", user_type)
        st.write("Current Reputation: ", balance + stake)
        st.write("Current Balance: ", balance)
        if st.session_state.user_type == "Auditor":
            st.write("Currrent Stake in Network = ", stake)
        
        
        with st.expander("Click to view private key"):
            st.markdown(private_key.replace("\n", "<br>"),unsafe_allow_html=True)
            
        with st.expander("Click to view public key"):
            st.markdown(public_key.replace("\n", "<br>"),unsafe_allow_html=True)