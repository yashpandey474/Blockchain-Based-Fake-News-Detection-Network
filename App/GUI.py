import streamlit as st
from pyblock.blockchain.blockchain import *
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
from become_validator import *
from vote_on_block import *
from upload_file import *
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

screen_functions = {
    "enter": enter,
    "login": login,
    "main_page": main_page,
    "account_info": show_account_info,
    "show_transac": show_transactions,
    "show_blocks": show_blocks_news,
    "sign_up": sign_up,
    "sign_up_generate": sign_up_generate,
    "become_validator": become_validator,
    "vote_on_block": vote_on_block,
    "upload_file": upload_file
}

def main():
    print("CURRENT SCREEN = ", st.session_state.screen)
    
    if st.session_state.screen in screen_functions:
        screen_functions[st.session_state.screen]()
    
    else:
        screen_functions["enter"]()
        

if __name__ == "__main__":
    if "screen" not in st.session_state:
        
        print("SCREEN INITILIASED")
        st.session_state.initialise = False
    
        st.session_state.gen_key_pressed = False
        
        st.session_state.validator = False
        
        st.session_state.block_proposer = None
        
        st.session_state.block_recieved = False
        
        st.session_state.recieved_block = None
        
        st.session_state.verified = False
        
        st.session_state.previous_screen = "enter"
        
        st.session_state.screen = "enter"
        
        
    main()
        
