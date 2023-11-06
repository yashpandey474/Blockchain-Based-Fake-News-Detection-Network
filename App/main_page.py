# STREAMLIT GUI
import streamlit as st
from change_screen import *
from ..pyblock.wallet.transaction import *
from ..pyblock import config
from ..pyblock.blockchain.block import *

def main_page():
    # st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, user.")

    if st.button("Upload New News"):
        # GET UPLOADED TEXT FILE
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

        if uploaded_file:
            # CREATE PARTIAL TRANSACTION
            partial_transaction = Transaction.generate_from_file(
                sender_wallet=st.session_state.p2pserver.wallet, file=uploaded_file)

            # BROADCASE NEWLY CREATED TRANSACTION
            st.session_state.p2pserver.broadcast_transaction(
                partial_transaction)

    # VIEW NEWS STORED IN BLOCKCHAIN
    if st.button("View all Verified News"):
        change_screen("show_blocks")

    if st.button("View Account Information"):
        change_screen("account_info")

    if st.session_state.user_type == "Auditor":
        if st.button("View all transactions in mempool"):
            change_screen("show_transac")

        if st.button("Become a Validator."):
            if st.session_state.validator:
                st.write("You are already a validator.")

            else:
                current_balance = st.session_state.accounts.get_balance(
                    st.session_state.wallet.public_key)

                if current_balance < config.MIN_STAKE:
                    st.write("You don't have enough balance to stake.")

                else:
                    st.session_state.try_be_validator = True

        if st.session_state.try_be_validator:
            st.write("Please enter an amount to stake.")
            st.write("Minimum Stake Required: ", config.MIN_STAKE)
            st.write("Your Current Balance: ", current_balance)
            st.session_state.numerical_value = st.number_input(
                "Enter a numerical value", min_value=config.MIN_STAKE, max_value=current_balance, value=config.MIN_STAKE, step=1)

            if st.button("Submit Stake"):
                st.session_state.p2pserver.broadcast_new_validator(
                    stake=st.session_state.numerical_value)
                st.write("You are successfully registered as a validator.")
                st.session_state.validator = True

                time.sleep(1)
                st.session_state.try_be_validator = False

    # IF THE USER IS A VALIDATOR AND CURRENT BLOCK PROPOSER
    if st.session_state.validator and st.session_state.block_proposer == st.session_state.wallet.public_key:
        # SHOW TRANSACTION POOL AND ASK TO CHOOOSE TRANSACTIONS
        table_data = []
        transactions = st.session_state.p2pserver.transaction_pool.transactions
        transaction_dict = {
            transaction.id: transaction for transaction in transactions
        }

        for transaction in transactions:
            table_data.append({
                "ID": transaction.id,
                "IPFS Address": transaction.ipfs_address,
                "Model Score": transaction.model_score,
                "Sender Reputation": transaction.sender_reputation
            })

        max_selections = config.BLOCK_TRANSACTION_LIMIT

        # DISPLAY TABLE OF TRANSACS. WITH SELECT BOX
        selected_transactions = st.multiselect(
            "Select transactions",
            table_data,
            default=[],
            key="transactions",
        )

        # WARN USER IF MORE THAN ALLOWED TRANSACTIONS SELECTED
        if len(selected_transactions) > max_selections:
            st.warning(
                f"Maximum selections allowed: {max_selections}. Please deselect items."
            )

        # CONFIRM THE SELECTION
        if st.button("Confirm Selection") and len(selected_transactions) <= max_selections:
            selected_transaction_objects = [
                transaction_dict[transaction["ID"]] for transaction in selected_transactions
            ]

            # CREATE A BLOCK WITH TRANSACTIONS [PASSED AS LIST]
            block = Block.create_block(
                lastBlock=st.session_state.blockchain.chain[-1],
                _data=selected_transaction_objects,
                wallet=st.session_state.p2pserver.wallet,
                blockchain=st.session_state.blockchain
            )

            # BROADCAST THE BLOCK
            st.session_state.p2pserver.broadcast_block(block)

            # CONFIRMATION MESSAGE
            st.write(
                "The created block was transmitted. Waiting for confirmations.")

            st.session_state.block_confirmations = 0

    if st.session_state.validator:
        st.write("Current Block Proposer: ", st.session_state.block_proposer)

    if "block_confirmations" in st.session_state and st.session_state.block_confirmations >= 0:
        st.write("Current Confirmations: ",
                 st.session_state.block_confirmations)

    # IF RECEIVED A BLOCK
    if st.session_state.block_received:
        # SHOW THE BLOCK'S TRANSACTIONS AND ASK FOR VOTES
        st.header("Block Info")
        st.write("Validator:", block.validator)
        st.write("Timestamp:", block.timestamp)
        st.header("Vote on Transactions")
        block = st.session_state.received_block
        transaction_votes = {}
        table_data = []

        for transaction in block.data:
            transaction_id = transaction.id
            vote = st.radio(
                f"Vote for Transaction {transaction_id}", ("True", "False"))
            transaction_votes[transaction_id] = vote

            table_data.append({
                "ID": transaction.id,
                "IPFS Address": transaction.ipfs_address,
                "Sender Address": transaction.sender_address,
                "Sender Reputation": transaction.sender_reputation,
                "Model Score": transaction.model_score,
                "Sign of Sender": transaction.sign,
                "Vote": vote,
            })

        st.table(table_data)

        if st.button("Submit Votes"):
            # BROADCAST THE VOTES
            st.session_state.p2pserver.broadcast_votes(
                transaction_votes)

            st.write("Votes Submitted. Thank you")

            time.sleep(1)

            st.session_state.block_received = False

        # GO TO PREVIOUS SCREEN
        if st.button("Back"):
            # Set the previous screen in the session state
            change_screen(st.session_state.previous_screen)

    