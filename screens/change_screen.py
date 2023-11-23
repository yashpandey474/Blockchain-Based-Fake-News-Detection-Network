# CHANGE THE SCREEN OF GUI
import streamlit as st
from extra.config import BLOCK_VALIDATOR_CHOOSE_INTERVAL, START_TIME
import time
import asyncio

auditors_guidelines = """
        ### Auditor Guidelines
        
        As an auditor, you play a vital role in our trusted private network. Here's what you do:
        
        - **Stake Reputation:** Stake some "reputation" to become a validator in the network.
        
        - **Block Proposal:** If chosen as a block proposing validator, select transactions for a new block. If the majority of validators (>50%) agree, the block is added, and you earn reputation.
        
        - **Voting on News:** Vote on news in incoming blocks labeled "Fake" or "True". A machine learning model provides a score (0-1) for the probability of fake news, alongside the sender's reputation.
        
        Your contributions help maintain network integrity and ensure the authenticity of shared news.
"""

readers_guidelines = """
### Guidelines for Readers:

As a reader in our network, you have the privilege to access and explore the news posted on our consortium blockchain. Here's what you can do:

1. **Anonymous Exploration:** Anonymously view news posted on the network without the need for authentication.

2. **Access Metrics:** Access essential information about news posts, including title, content, machine learning model score indicating the probability of fake news, percentage of auditors who voted the news as fake, and sender reputation.

3. **Stay Informed:** Engage with informative news content while being aware of the authenticity metrics provided.

4. **Contribute to Data Availability:** Contribute indirectly by generating data through your viewership, aiding in the creation of a more informed network environment.
"""

vote_on_block_message =            """
    # Vote on Received Block

    This section allows you to vote on the block proposed within the network.

    ## Block Information:

    Here are the details of the proposed block:

    - **Validator:** [Validator's Public Key]
    - **Timestamp:** [Timestamp of Block]
    - **Validator Reputation:** [Validator's Reputation]

    ## Transactions in Block:

    Below, you'll find the transactions included in the proposed block along with their details:

    """
    
view_block_status_message = """
            ## Block Proposer Responsibilities
            
            As the block proposer in our trusted network, your role is crucial:
            
            - **Transaction Selection:** Choose credible transactions relevant to the network. 
            
            - **News Voting:** Ensure fair and accurate voting on news credibility.
            
            - **Block Creation:** Once satisfied, create and broadcast the block to the network.
            
            Remember, your actions shape the integrity of the network's information.
            """

show_transactions_message = """
            ## Current Transactions in Mempool

            Welcome to the 'Current Transactions in Mempool' section.

            - View the current transactions pending in the network's mempool.
            - Each transaction contains various details such as the sender's reputation, stake, model score, etc.
            - Review the transaction details and their associated content.
            - Explore the titles and text to identify pending news in the network's mempool.
            
            Stay updated with the latest transactions within the network!
            """

upload_file_message = """
    ## Upload News Guidelines
    
    As an anonymous user or an auditor of the network, you have the privilege to upload news to the network. 
    Please ensure the following when uploading news:
    
    - **File Format:** Upload a text file (.txt) containing the news article or information.
    
    - **Transaction Fee:** Optionally, you can include a transaction fee to prioritize your news on the network. 
      Ensure the fee is within your available balance.
    
    - **Authentication:** Anonymous uploaders must abide by network guidelines and refrain from uploading fake news as this would lead to reputation penalties.
    
    By contributing news, you help maintain a diverse and informative network for all users.
    """
    
view_sent_news_message = """
            ## News Broadcasted by You

            Welcome to the 'News Broadcasted' section.

            - View the transactions you have broadcasted to the network.
            - Review the transaction details and their associated content.
            - Know if the transaction has been confirmed by the network's auditors
            
            """

view_account_info_message = """
            ## ACCOUNT INFORMATION

            Welcome to the Account Information section.

            Here, you can find details about your account on the network:
            - **Reputation**: Your current reputation calculated as the sum of your balance and stake.
            - **Balance**: The current balance available in your account.
            - **Stake (for Auditors)**: If you're an auditor, this displays your stake in the network.
            - **Private Key**: Click to view your private key (This should be kept confidential).
            - **Public Key**: View your public key for identification in the network.

            Keep your private key secure and never share it with anyone!
            """

view_block_news_message = """
            ## View All Verified News

            Welcome to the 'View All Verified News' section.

            - Navigate through the sidebar options to explore.
            - This section presents details of all verified news available in the blockchain.
            - The table showcases various information:
              - Model Fake Score
              - Percentage of Fake and True Votes
              - Transaction and Block Creation Times
              - IPFS Address
              - Sender's Public Key
              - Validator's Public Key
              - Sender's Reputation
            - Click the 'QR Code' button to generate a QR code for each transaction.

            Dive in to explore the verified news available in the blockchain and stay informed!
            """
    
blocks_broadcasted_message = """
            # Blocks Broadcasted by You

            This page displays the blocks that you have broadcasted within the network.

            ## Block Broadcast Log:

            Below is a log containing the details of blocks you've broadcasted:

            """

navbar_style = """
            <style>
            .stRadio p{
                font-size: 20px;
            }
            .stRadio>label>div>p{
                font-size: 24px;
            }
            </style>
            """
            
reputation_log_message = """
    # Log of Your Reputation Changes

    This page displays the log of your reputation changes within the network. Your reputation may change due to various reasons outlined below:

    ### Reasons for Reputation Changes:

    - **Initial Reputation Allocation**:
      Upon joining the network, users receive an initial reputation value. Auditors receive a notably higher reputation than readers, following successful authentication.

    - **Broadcasting News**:
      If the majority of auditors mark news as "Fake," the broadcaster faces a penalty proportionate to their balance. Conversely, if marked "True," the broadcaster receives a balance increase, but not proportionate to their existing balance to prevent disproportionate wealth accumulation.

    - **Block Validation**:
      Auditors that voted on a news post to be “Fake”/”True” and the majority voted for the opposite are penalized by a percentage of their stake in the network.

    - **Not Proposing a Block**:
      Block proposers that fail to utilize network time by creating a new block within the allotted time period are penalized on a percentage of their stake.

    ### Reputation Change Log:

    Below is a table displaying the details of your reputation changes:
    """
    
# General Message for the Enter Page
enter_page_message = """
### Welcome to our Consortium Blockchain Network!

Explore, learn, and engage responsibly with the news shared on our network. Anonymously browse through the latest posts and stay informed about each news item's authenticity metrics. Your viewership contributes to the generation of a transparent and informed network environment.

Discover the power of reliable information dissemination and responsible engagement within our network. Dive in, explore, and be part of a community fostering informed insights!
"""

entered_pages = set([
    "main_page",
    "account_info",
    "show_transac"
    "show_blocks",
    "become_validator",
    "vote_on_block",
    "upload_file",
    "view_sent_news",
    "vote_on_block",
    "view_block_status",
    "propose_block",
    "view_sent_blocks",
    "view_log_reputation"
])


if "validator" not in st.session_state:
    st.session_state.validator = False

navigation_options = {
    "Reader": ("Main Page", "Upload News", "Verified News", "Account Info", "Sent News", "Reputation Log"),
    "Auditor": (
        "Main Page", "Upload News", "Verified News", "Account Info", "Sent News", "Reputation Log", "Transactions in Mempool",
        "Manage Stake in Network",
        "Current Block Status", "Broadcasted Blocks"
    )
}

screen_mapping = {
    "Main Page": "main_page",
    "Upload News": "upload_file",
    "Verified News": "show_blocks",
    "Account Info": "account_info",
    "Sent News": "view_sent_news",
    "Reputation Log": "view_log_reputation",
    "Transactions in Mempool": "show_transac",
    "Manage Stake in Network": "become_validator",
    "Current Block Status": "view_block_status",
    "Broadcasted Blocks": "view_sent_blocks",
    "Enter Page": "enter"
}


def add_space():
    # ADD SPACE
    for i in range(30):
        st.empty()


def change_screen_navbar(nav_selection):
    # Map the nav_selection to corresponding actions
    screen = screen_mapping.get(nav_selection)
    
    if screen:
        
        
        #IF GOING TO BECOME VALIDATOR PAGE
        if nav_selection == "Manage Stake in Network":
            st.session_state.stake_submitted = False

        #IF GOING TO UPLOAD FILE PAGE
        if nav_selection == "Upload News":
            st.session_state.upload_file_executed = False

        #CHANGE THE SCREEN
        with st.spinner("Please Wait"):
            change_screen(screen)


async def watch(test):
    while True:
        if st.session_state.screen_changed:
            break

        current_time = int(time.time())
        time_elapsed = current_time - START_TIME.timestamp()
        time_remaining = BLOCK_VALIDATOR_CHOOSE_INTERVAL - \
            (time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL)
        test.markdown(
            f"""
            <div class="time" style="font-size: 25px;text-align: center;color: black; background-color: white; style:bold;">
                Time Remaining in Current Block Proposing Period: {str(time_remaining)}
            </div>
            """, unsafe_allow_html=True)
        await asyncio.sleep(1)


def change_screen(input_string):
    print("CHANGE SCREEN CALLED ", input_string)
    
    if input_string == "sign_up_generate":
        st.session_state.main_pressed = False
        st.session_state.gen_key_pressed = False
        
    if input_string == "enter":
        st.session_state.main_pressed = False
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.initialise = False
        st.session_state.user_type = "Reader"

    st.session_state.screen_changed = True
    st.session_state.previous_screen = st.session_state.screen
    st.session_state.screen = input_string
    st.rerun()
