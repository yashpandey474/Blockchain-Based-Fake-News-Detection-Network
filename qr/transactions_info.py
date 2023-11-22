# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
from datetime import datetime

from .qr_handler import make_qr


def show_transaction(transaction, show = 0):
    percent_fake_votes = 100*(len(transaction.negative_votes) /
                              (len(transaction.negative_votes) + len(transaction.positive_votes)))

    data = f"""
Model Fake Score: {transaction.model_score},
Percent of Fake Votes: {str(percent_fake_votes) + "%"},
Percent of True Votes: {str(100 - percent_fake_votes)  + "%"},
Transaction Creation Time: {datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y")},
Sender Reputation: {transaction.sender_reputation},
Content URL: https://{transaction.ipfs_address}.ipfs.dweb.link
    """

    return make_qr(data, show, transaction.ipfs_address)
