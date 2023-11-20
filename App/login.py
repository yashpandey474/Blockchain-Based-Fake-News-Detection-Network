import streamlit as st
import change_screen
from enter import *
import crypto_logic
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
            vc = crypto_logic.verify(user_input)

            if vc[0]:
                # st.markdown(f'<span style="color:green"><b><i>{vc[1]}</b></i></span>', unsafe_allow_html=True)
                initialise(vc[2])
                with st.spinner("Please Wait"):
                    change_screen.change_screen("main_page")

            else:
                # st.markdown(f'<span style="color:yellow"><b>{vc[1]}</b></span>', unsafe_allow_html=True)
                st.error(vc[1])
        else:
            st.markdown('<span style="color:yellow"><b>Key Not Provided</b></span>', unsafe_allow_html=True)

    b1= st.button("Sign up instead")
    b2 = st.button("Exit Screen")
    
    if b1:
        with st.spinner("Please Wait"):
            change_screen.change_screen("sign_up")
    elif b2:
        with st.spinner("Please Wait"): 
            change_screen.change_screen("enter")

    # if st.button("Ba ck"):
    #     with st.spinner("Please Wait"): change_screen.change_screen(st.session_state.previous_screen)
