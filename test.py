import streamlit as st
import datetime
import time
import pyblock.config as config

def block_logic():
    #IF > 50% VOTES RECEIVED
    total_active_accounts = len(st.session_state.p2pserver.accounts.get_active_accounts())
    if st.session_state.received_block.votes >= 0.5 * (total_active_accounts):
        #REMOVE THE TRANSACTIONS FROM THE MEMPOOL
        st.session_state.p2pserver.transaction_pool.remove(st.session_state.received_block.data)
        
        #ADD THE BLOCK TO THE BLOCKCHAIN
        st.session_state.blokchain.chain.append(st.session_state.received_block)
        

def seconds_until_next_check(start_time, interval):
    current_time = datetime.datetime.now()
    delta_seconds = (current_time - start_time).total_seconds()
    seconds_to_next_check = interval - (delta_seconds % interval)
    if seconds_to_next_check < 5:  # Adding a small buffer
        seconds_to_next_check += interval
    return seconds_to_next_check

# Streamlit app main function


def main():
    # Set the start time in session state if not set
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = datetime.datetime.now()

    # Initialize 'show_popup' state
    if 'show_popup' not in st.session_state:
        st.session_state['show_popup'] = False

    st.title('Time Check App')

    # Check if we should show the popup
    if st.session_state['show_popup']:
        st.balloons()  # Show a celebratory popup
        st.session_state['show_popup'] = False  # Reset the popup flag

    # Continuously update the session state to check the time
    with st.empty():
        while True:
            # Sleep until next check
            time.sleep(seconds_until_next_check(
                config.START_TIME, config.BLOCK_VALIDATOR_CHOOSE_INTERVAL))
            print(int(time.time()))
            st.session_state['show_popup'] = True
            st.experimental_rerun()

#time and previous block hash

if __name__ == "__main__":
    main()
