import streamlit as st
from pyblock import config
import change_screen as change_screen_

def become_validator():
    if st.session_state.screen == "become_validator":
        
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
        
        if st.session_state.validator:
            st.write("You are already a validator.")
        
        elif not st.session_state.stake_submitted:
            st.session_state.stake = 0

        #GET CURRENT BALANCE
        st.session_state.balance = st.session_state.p2pserver.accounts.get_balance(
        st.session_state.wallet.get_public_key()
            )
        st.markdown(
    """
    # Manage Stake in Network

    This section allows you to manage your stake in the network.
    If you are a Validator, you can modify your current stake; otherwise, you can stake to become a Validator.

    ## Your Current Status:

    - **User Type:** [User Type: Reader/Auditor]
    - **Current Balance:** [Your Current Balance]
    - **Minimum Stake Required:** [Minimum Stake Required]

    ## Stake Management:

    If you are not already a Validator, you can stake a certain amount to become one.
    If you are a Validator, you can modify your existing stake.

    """
)
        #IF NOT ENOUGH BALANCE
        if st.session_state.balance  + st.session_state.stake < config.MIN_STAKE:
            st.error(f"You don't have enough balance to stake. Minimum Stake Required: {config.MIN_STAKE}")

        else:
            st.write("Minimum Stake Required: ", config.MIN_STAKE)
            st.write("Your Current Balance: ", st.session_state.balance)
                
            if st.session_state.validator:
                st.write("Your Current Stake: ", st.session_state.stake)
                
                #GET VALUE TO STAKE
            if not st.session_state.stake_submitted:
                stake = st.number_input(
                            "Amount to stake in VRC",
                            min_value=config.MIN_STAKE, 
                            max_value=int(st.session_state.balance+st.session_state.stake),
                            value=max(config.MIN_STAKE, st.session_state.stake),
                            step=1
                    )

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
                    st.session_state.stake = stake
                        
                        #BROADCAST TO REMAINING PEERS OF NEW VALIDATOR
                    if old_stake != st.session_state.stake:
                        with st.spinner("Please Wait.."):
                            st.session_state.p2pserver.broadcast_new_validator(
                                        stake = st.session_state.stake
                            )
                            
                    st.session_state.stake_submitted = True
                    st.rerun()
                    
            
            
            else:
                if not st.session_state.validator:
                    st.success(
                            f"You are successfully registered as a validator with stake: {st.session_state.stake}")
                    st.session_state.validator = True

                else:
                    st.success(f"Your stake has been successfully modified to: {st.session_state.stake}")
                        
            