import threading
import time
import streamlit as st

def background_task():
    while True:
        current_time = int(time.time())
        specified_time = 0 # Specify your target time here

        # Calculate the difference in seconds
        time_difference = current_time - specified_time

        # Check if the time difference is a multiple of 2 minutes (120 seconds)
        if time_difference % 120 == 0:
            st.session_state.validation_time = True
            
            #CALL THE FUNCTION TO CHOOSE A BLOCK PROPOSER AND SET AS CURRENT BLOCK PROPOOSER
            # TODO: FINALISE THE SEED VALUE
            st.session_state.block_proposer = st.session_state.accounts.choose_validator(seed = current_time)
        else:
            st.session_state.validation_time = False

        # Sleep for a short duration before checking again (adjust as needed)
        time.sleep(30)  # Check every 30 seconds



