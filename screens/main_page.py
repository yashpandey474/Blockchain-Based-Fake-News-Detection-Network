# STREAMLIT GUI
import streamlit as st
import change_screen as change_screen_

def main_page():
    user_type = st.session_state.user_type
    
    navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
    st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
    selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
    if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
        change_screen_.change_screen_navbar(selected_option)
        
    welcome_message = f"Welcome, {st.session_state.name}!"

    st.markdown(f"## {welcome_message}")
    
    if user_type == "Auditor":
        st.markdown(change_screen_.auditors_guidelines)
        
    else:
        st.markdown(change_screen_.readers_guidelines)
        
        
    # if st.button("Exit Application"):
    #     st.session_state.p2pserver.flag = True
    #     change_screen_.change_screen("enter")
        
    
        