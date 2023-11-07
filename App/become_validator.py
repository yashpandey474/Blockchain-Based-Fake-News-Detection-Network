import streamlit as st
from pyblock import config
from change_screen import *

def become_validator():
    if st.session_state.validator:
        st.write("You are already a validator.")

    else:
        current_balance = st.session_state.p2pserver.accounts.get_balance(
            st.session_state.wallet.get_public_key()
        )

        if current_balance < config.MIN_STAKE:
            st.write("You don't have enough balance to stake. Minimum Stake Required: ", config.MIN_STAKE)

        else:
            st.write("Minimum Stake Required: ", config.MIN_STAKE)
            st.write("Your Current Balance: ", current_balance)
            st.session_state.numerical_value = st.number_input(
                "Amount to stake in VRC", min_value=config.MIN_STAKE, max_value=current_balance, value=config.MIN_STAKE, step=1)

            if st.button("Submit Stake"):
                st.session_state.p2pserver.broadcast_new_validator(
                        stake=st.session_state.numerical_value
                )
                st.write("You are successfully registered as a validator.")
                st.session_state.validator = True
                
    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
