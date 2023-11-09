# from flask import Flask, request, jsonify, redirect
# import time
# from App.pyblock.blockchain.blockchain import Blockchain
# from App.pyblock.wallet.wallet import Wallet
# from App.pyblock.wallet.transaction_pool import TransactionPool
# from App.pyblock.p2pserver import P2pServer
# import App.pyblock.config as config
# import threading
# import streamlit as st
# app = Flask(__name__)

# HTTP_PORT = int(config.HTTP_PORT)

# blockchain = st.session_state.p2pserver.blockchain
# # Using current timestamp as seed for wallet
# wallet = st.session_state.p2pserver.wallet
# transaction_pool = st.session_state.p2pserver.transaction_pool
# p2pserver = P2pServer(blockchain, transaction_pool, wallet)


# @app.route('/blocks', methods=['GET'])
# def get_blocks():
#     return jsonify([block.to_json() for block in blockchain.chain])


# @app.route('/transactions', methods=['GET'])
# def get_transactions():
#     return jsonify(transaction_pool.transactions)


# @app.route('/transact', methods=['POST'])
# def post_transact():
#     data = request.json
#     to = data['to']
#     amount = data['amount']
#     type_ = data['type']
#     transaction = wallet.create_transaction(
#         to, amount, type_, blockchain, transaction_pool)
#     p2pserver.broadcast_transaction(transaction)
#     return redirect('/transactions')


# @app.route('/bootstrap', methods=['GET'])
# def bootstrap_system():
#     p2pserver.bootstrap_system()
#     return jsonify(message="System bootstrapped")


# @app.route('/public-key', methods=['GET'])
# def get_public_key():
#     return jsonify(publicKey=wallet.public_key)


# @app.route('/balance', methods=['GET'])
# def get_balance():
#     return jsonify(balance=blockchain.get_balance(wallet.public_key))


# def run_p2pserver():
#     print("Running p2p server on port: "+str(config.P2P_PORT))
#     p2pserver.listen()

# def runhttpserver():
#     print("Running http server on port: "+str(HTTP_PORT))
#     app.run(port=HTTP_PORT, debug=False, host="0.0.0.0")

