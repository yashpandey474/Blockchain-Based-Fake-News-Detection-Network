import streamlit as st
from  change_screen import *
from pyblock.chainutil import *
from enter import *
import crypto_logic
import re


def sign_up_generate():
    if st.session_state.screen == "sign_up_generate":
        st.markdown(
            f"<h1 style='text-align: center;'>Sign Up as a {st.session_state.user_type}</h1>",
            unsafe_allow_html=True
        )

        # Add buffer text to span the whole page
        col1, col2, col3 = st.columns([1, 20, 1])
        with col2:
            if st.session_state.user_type == "Auditor":
                st.write("""As an auditor, you participate in our trusted private network. 
                     You must stake some "reputation" to become a validtor in the network. 
                     If you are chosen as a block proposing validator, you must choose some
                     transactions to include in a new block which is transmitted to other validators
                     and if  >=50\% of validators want the block to be included in the chain, it is added 
                     and you are rewarded with some reputation value. As a validator, you
                     would also (in addition to being in contention for becoming a block proposer) 
                     be able to vote on news in incoming blocks that other auditors chose to include 
                     as "Fake" or "True". A machine learning model is deployed that provides a
                     score from 0 to 1 as the probability of the news being fake according to our training data, this score
                     along with the reputation of the sender is available with every news received.
                     """)  # Modify this with your intended text

        # GENERATE A NEW PRIVATE KEY FOR USER
        if st.button("Generate a new Private Key"):
            st.session_state.gen_key_pressed = True
            
            with st.spinner("Please Wait.."):
                private_key = crypto_logic.gen_sk()
            
            st.success("Generated Private key. Please store it safely.")

            # PRINT THE PRIVATE KEY
            with st.expander("Click to view private key"):
                kk = private_key.export_key().decode()
                kk = kk.replace("\n", "<br>")
                st.markdown(kk, unsafe_allow_html=True)

            # INITIALISE ACCOUNT & WALLET OF SESSION
            initialise(private_key)

        if st.session_state.gen_key_pressed:
            if st.button("Go to main"):
                with st.spinner("Please Wait"):
                     change_screen.change_screen("main_page")
                st.session_state.gen_key_pressed = False

        if st.button("Back"):
            with st.spinner("Please Wait"): 
                change_screen.change_screen("sign_up")
                
        change_screen.add_space()

def sign_up():
    if st.session_state.screen == "sign_up":
        st.title("Sign Up as a " + st.session_state.user_type)

        default_name = "Amitesh Singh Rajput"
        default_email = "amitesh.singh@pilani.bits-pilani.ac.in"
        default_certificate_id = "ABCD"

        name = st.text_input("Enter Your Name", value=default_name)
        email = st.text_input("Enter Your Email", value=default_email)

        if st.session_state.user_type == "Auditor":
            certificate_id = st.text_area(
                "Enter the SGX Certificate ID", value=default_certificate_id)

        if st.button("Submit Details"):
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(pattern, email):
                st.warning("Invalid Email ID")
                
            else:
                if st.session_state.user_type == "Auditor" and not crypto_logic.verify_certificate(certificate_id):
                    st.warning("Invalid Certificate ID")
                else:
                    st.session_state.name = name
                    st.session_state.email = email
                    with st.spinner("Please Wait"):
                         change_screen.change_screen("sign_up_generate")

        # GO TO PREVIOUS SCREEN
        if st.button("Back"):
            with st.spinner("Please Wait"):
                 change_screen.change_screen("login")
            