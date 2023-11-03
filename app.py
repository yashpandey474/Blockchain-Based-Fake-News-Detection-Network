import streamlit as st
from GUI import main
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
import pyblock.config as config
import threading

#INSTANTIATE IN CLASS
blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()
p2pserver = P2pServer(blockchain, transaction_pool, wallet)

#START LISTENING ON P2P SERVER
def run_p2pserver():
    print("Running p2p server on port: "+str(config.P2P_PORT))
    p2pserver.listen()

def start():
    p2p_thread = threading.Thread(target=run_p2pserver)
    p2p_thread.start()
    main()
    
