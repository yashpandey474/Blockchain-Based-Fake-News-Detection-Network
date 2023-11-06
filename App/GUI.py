import streamlit as st
from pyblock.blockchain.blockchain import Blockchain
from pyblock.blockchain.block import *
from pyblock.blockchain.account import *
from login import *
from main_page import *
from sign_up import *
from show_block_news import *
from show_transactions import *
from enter import *
from change_screen import *
from account_info import *
background_style = '''<style>
section {
background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmxvY2tjaGFpbnxlbnwwfHwwfHx8MA%3D%3D");
background-size: cover;
background-position: center;
transition: transform 0.3s ease-in-out;
width: 100%;
height: 100vh;
}
</style>
<script>
        const sections = document.querySelectorAll("section");
    sections.forEach(section => {
        section.addEventListener("mousemove", function(e) {
            const width = section.offsetWidth;
            const height = section.offsetHeight;
            const offsetX = 0.5 - e.pageX / width;
            const offsetY = 0.5 - e.pageY / height;
            section.style.transform = "perspective(1000px) rotateX(" + (offsetY * 4) + "deg) rotateY(" + (offsetX * 4) + "deg)";
        });
        section.addEventListener("mouseleave", function() {
            this.style.transform = "none";
        });
    });
    </script>
'''

st.markdown(background_style, unsafe_allow_html=True)


# st.markdown(
#     """
#     <iframe
#       src="HTML/custom_background.html"
#       width="100%"
#       height="100%"
#     >
#     </iframe>
#     """,
#     unsafe_allow_html=True,
# )
st.title("Fake News Detection System Utilising Blockchain")


def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen == "enter":
        print("CALL: ENTER")
        enter()
    if st.session_state.screen == "login":
        print("CALL: LOGIN")
        login()
            
    if st.session_state.screen == "main_page":
        print("YES. WE TRIED TO CALL THE MAIN PAGE")
        main_page()
            
    if st.session_state.screen == "account_info":
        print("CALL: ACC INFO")
        show_account_info(wallet= st.session_state.wallet, blockchain= st.session_state.blockchain)
        
    if st.session_state.screen == "show_transac":
        print("CALL: SHOW TRANSAC")
        show_transactions(transaction_pool = st.session_state.transaction_pool)
            
    if st.session_state.screen == "show_blocks":
        print("CALL: SHOW BLOCKS")
        show_blocks_news()

    if st.session_state.screen == "sign_up":
        sign_up()
        

if __name__ == "__main__":
    if "screen" not in st.session_state:
        
        print("SCREEN INITILIASED")
        st.session_state.initialise = False
        
        st.session_state.screen = "enter"
        
        st.session_state.gen_key_pressed = False
        
        st.session_state.try_be_validator = False

        st.session_state.validator = False
        
    main()
        
