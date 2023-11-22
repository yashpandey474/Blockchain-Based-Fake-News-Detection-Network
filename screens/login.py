import streamlit as st
import change_screen as change_screen_
from enter import initialise
from extra import crypto_logic
import time

def login():
    
    st.markdown(
        f"<h2 style='text-align: center;'>Login as {st.session_state.user_type}</h2>",
        unsafe_allow_html=True
    )
    #GET PRIVATE KEY OF USER
    user_input = st.text_area("Enter your Private Key")

    #SUBMIT
    if st.button("Submit key"):
        
        #IF PRIVATE KEY ENTERED
        if user_input:
            with st.spinner("Verifying Key"):
                vc = crypto_logic.verify(user_input)

            if vc[0]:
                with st.spinner("Initialising Your Account"):
                    initialise(vc[2])
                    while not st.session_state.p2pserver.initialised:
                        pass
                    st.write("Server Initialised. Waiting for connections..")
                    
                progress_bar = st.progress(0)
                for i in range(1, 101): 
                    time.sleep(0.02)  
                    progress_bar.progress(i)
                    
                change_screen_.change_screen("main_page")
                st.session_state.gen_key_pressed = False

            else:
                st.error(vc[1])
        else:
            st.warning("Private Key Not Provided")
            
    b1= st.button("Sign up instead")
    b2 = st.button("Exit Screen")
    
    if b1:
        with st.spinner("Please Wait"):
            change_screen_.change_screen("sign_up")
    elif b2:
        with st.spinner("Please Wait"): 
            change_screen_.change_screen("enter")