import threading
import time
import streamlit as st
from pyblock import config


def background_task():
    while st.session_state.validator:
        current_time = int(time.time())
        specified_time = config.START_TIME # Specify your target time here

        # Calculate the difference in seconds
        time_difference = current_time - specified_time

        # Check if the time difference is a multiple of 2 minutes (120 seconds)
        if time_difference % (60 * config.BLOCK_VALIDATOR_CHOOSE_INTERVAL) == 0:
            st.session_state.validation_time = True
            
            #CALL THE FUNCTION TO CHOOSE A BLOCK PROPOSER AND SET AS CURRENT BLOCK PROPOOSER
            # TODO: FINALISE THE SEED VALUE
            st.session_state.block_proposer = st.session_state.accounts.choose_validator(seed = current_time)
        else:
            st.session_state.validation_time = False

        # Sleep for a short duration before checking again (adjust as needed)
        time.sleep(30)  # Check every 30 seconds



