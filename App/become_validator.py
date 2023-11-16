import streamlit as st
from pyblock import config
from change_screen import *

def become_validator():
        
    if st.session_state.validator:
        st.write("You are already a validator.")
    
    else:
        st.session_state.stake = 0

        #GET CURRENT BALANCE
    st.session_state.balance = st.session_state.p2pserver.accounts.get_balance(
    st.session_state.wallet.get_public_key()
        )

        #IF NOT ENOUGH BALANCE
    if st.session_state.balance  + st.session_state.stake < config.MIN_STAKE:
        st.error("You don't have enough balance to stake. Minimum Stake Required: ", config.MIN_STAKE)

    else:
        st.write("Minimum Stake Required: ", config.MIN_STAKE)
        st.write("Your Current Balance: ", st.session_state.balance)
            
        if st.session_state.validator:
            st.write("Your Current Stake: ", st.session_state.stake)
            
            #GET VALUE TO STAKE

        stake = st.number_input(
                    "Amount to stake in VRC",
                    min_value=config.MIN_STAKE, 
                    max_value=st.session_state.balance+st.session_state.stake,
                    value=max(config.MIN_STAKE, st.session_state.stake),
                    step=1
            )

            #SUBMT STAKE
        if st.button("Submit Stake"):
            old_stake = st.session_state.stake
            st.session_state.stake = stake
                
                #BROADCAST TO REMAINING PEERS OF NEW VALIDATOR
            if old_stake != st.session_state.stake:
                st.session_state.p2pserver.broadcast_new_validator(
                                stake = st.session_state.stake
                    )
                    
            if not st.session_state.validator:
                st.success(f"You are successfully registered as a validator with stake: {st.session_state.stake}")
                st.session_state.validator = True
                        
            else:
                st.success(f"Your stake has been successfully modified to: {st.session_state.stake}")
                        
        
    
    #GO BACK TO MAIN SCREEN
    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
