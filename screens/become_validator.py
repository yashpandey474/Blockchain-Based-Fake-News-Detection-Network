import streamlit as st
from extra import config
import change_screen as change_screen_

def become_validator():
    if st.session_state.screen == "become_validator":
        
        #NAVIGATION BAR
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
        
        
        #IF ALREADY A VALIDATOR: SHOW MESSAGE
        if st.session_state.validator:
            st.write("You are already a validator.")
        
        
        #IF NOT A VALIDATOR: 0 AS OLD STAKE
        else:
            st.session_state.stake = 0

        #GET CURRENT BALANCE
        st.session_state.balance = st.session_state.p2pserver.accounts.get_balance(st.session_state.wallet.get_public_key())
        
        user_type = ("Validating Auditor" if st.session_state.validator else st.session_state.user_type)
        
        #SHOW THE MESSAGE
        st.markdown(f"""
    # Manage Stake in Network

    This section allows you to manage your stake in the network.
    If you are a Validator, you can modify your current stake; otherwise, you can stake to become a Validator.

    ## Your Current Status:

    - **User Type:** {user_type}
    - **Current Balance:** {st.session_state.balance}
    - **Minimum Stake Required:** {config.MIN_STAKE}

    ## Stake Management:

    If you are not already a Validator, you can stake a certain amount to become one.
    If you are a Validator, you can modify your existing stake.

    """)
        

        #IF NOT ENOUGH BALANCE
        if st.session_state.balance  + st.session_state.stake < config.MIN_STAKE:
            st.error(f"You don't have enough balance to stake. Minimum Stake Required: {config.MIN_STAKE}")

        #IF HAS ENOUGH BALANCE
        elif st.session_state.balance  + st.session_state.stake >= config.MIN_STAKE:
            
            #IF ALREADY A VALIDATOR
            if st.session_state.validator:
                #DISPLAY CURRENT STAKE
                st.write("Your Current Stake: ", st.session_state.stake)
                
            #IF SUBMITTED STAKE: SUCCESSFUL MESSAGE
            if st.session_state.stake_submitted:
                
                #GET CURRENT STAKE IN NETWORK 
                stake = st.session_state.p2pserver.blockchain.get_stake(st.session_state.p2pserver.wallet.get_public_key())
                
                st.success(f"Your stake in the network is now: {stake}")
                    
                
            #IF HASNT SUBMITTED STAKE
            if not st.session_state.stake_submitted:
                #ASK FOR STAKE INPUT
                stake = st.number_input(
                            "Amount to stake in VRC",
                            min_value=config.MIN_STAKE, 
                            max_value=int(st.session_state.balance+st.session_state.stake),
                            value=max(config.MIN_STAKE, st.session_state.stake),
                            step=1
                    )

                #DISPLAY THE MESSAGE
                st.markdown(
                """
                Once you've decided on the stake amount, click the "Submit Stake" button to proceed. 
                If you've successfully modified or submitted your stake, you'll receive a confirmation message. 
                Thank you for your participation!
                """
                )
                
                #SUBMT STAKE
                if st.button("Submit Stake"):
                    old_stake = st.session_state.stake
                    
                    #BROADCAST TO REMAINING PEERS OF NEW VALIDATOR
                    if old_stake != stake:
                        #BROADCAST NEW VALIDATOR
                        with st.spinner("Notifying Network.."):
                            st.session_state.p2pserver.broadcast_new_validator(
                                        stake = stake
                            )
                        
                    #REMOVE THE BUTTONS FOR DEFINING STAKE
                    st.session_state.stake = stake
                    st.session_state.validator = True
                    st.session_state.stake_submitted = True
                    st.rerun()
                    
            
            