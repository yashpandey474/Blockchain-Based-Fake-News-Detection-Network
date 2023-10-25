import streamlit as st

def show_blockchain():
    st.title("FAKE NEWS DETECTION BLOCKCHAIN")
    st.write("Welcome to the blockchain system for fake news detection.")
    
    if st.button("Upload New News"):
        upload_news()
        
    if st.button("Contest for validation"):
        contest_validation()
        
    if st.button("View Account Information"):
        show_account_info()
        
        