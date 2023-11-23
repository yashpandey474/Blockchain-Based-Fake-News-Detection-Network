import streamlit as st
import change_screen as change_screen_
import pandas as pd


def view_log_reputation():
    if st.session_state.screen == "view_log_reputation":
        #SHOW NAVIGATION BAR
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(change_screen_.navbar_style, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
            
            
        #SHOW MESSAGE
        st.markdown(change_screen_.reputation_log_message)
        
        
        #SPINNNER FOR GETTING REPUTATION
        with st.spinner('Loading data...'):
            
          progress_bar = st.progress(0)  # Initialize progress bar
          log_reputation = st.session_state.p2pserver.accounts.accounts[
              st.session_state.p2pserver.wallet.get_public_key()
          ].reputation_changes
          
          table_data = []
          total_records = len(log_reputation)
          
          for i, (reason, amount) in enumerate(log_reputation):
              table_data.append({
                  "Change Reason": reason,
                  "Change Amount": amount
              })
              progress = (i + 1) / total_records
              progress_bar.progress(progress)  # Update progress bar

          progress_bar.empty()  # Remove progress bar when done

        st.dataframe(pd.DataFrame(table_data), height=500)
          
          
          
          
          
          