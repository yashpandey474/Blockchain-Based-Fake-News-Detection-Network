import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from ipfs.ipfs_handler import IPFSHandler
def view_sent_news():
    if st.session_state.screen == "view_sent_news":
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
            
        st.markdown(
            change_screen_.view_sent_news_message,
            unsafe_allow_html=True
        )
        
        sent_transactions = st.session_state.p2pserver.accounts.get_sent_transactions(
            st.session_state.p2pserver.wallet.get_public_key()
        )

        if len(sent_transactions) < 1:
            st.write(
                "You haven't broadcasted any news in the network yet.")

        else:
            table_data = []
            
            progress_bar = st.progress(0)
            current_progress = 1
            i = 1
            total_transactions = len(sent_transactions)
            
            for transaction in sent_transactions:
                status_pool = st.session_state.p2pserver.transaction_pool.transaction_exist(transaction)
                # content = IPFSHandler.get_from_ipfs(transaction.ipfs_address)
                
                transaction_data = {
                        "Status": "",
                        "Model Score": transaction.model_score,
                        "Transaction Fee": transaction.fee,
                        "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                        # "Title": content.split("\n")[0],
                        "Content URL": "https://"+ transaction.ipfs_address +".ipfs.dweb.link",
                        "ID": transaction.id
                }
                
                if status_pool:
                    transaction_data["Status"] = "Unconfirmed"
                    
                else:  
                    transaction_data["Status"] = "Added to Blockchain Network"
                    
                    chain = st.session_state.p2pserver.blockchain.chain
                    for block in chain:
                        for verified_transaction in block.transactions:
                            if transaction.id == verified_transaction.id:
                                percent_fake_votes = 100*(len(verified_transaction.negative_votes)/(len(verified_transaction.negative_votes) + len(verified_transaction.positive_votes)))
                                transaction_data["Percent of Fake Votes"] = str(percent_fake_votes) + "%"
                                transaction_data["Percent of True Votes"] = str(100 - percent_fake_votes)  + "%"
                                transaction_data["Total Votes"] =  len(verified_transaction.positive_votes) + len(verified_transaction.negative_votes),


                current_progress = int((i / total_transactions) * 100)
                progress_bar.progress(current_progress)
                i += 1
                table_data.append(transaction_data)
                
            # t.empty()
            progress_bar.empty()
            st.write("Transactions loaded successfully!")
            st.dataframe(pd.DataFrame(table_data), height=500)

        
        