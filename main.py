from flask import Flask, request, jsonify, redirect
import time
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from pyblock.p2pserver import P2pServer
import pyblock.config as config
import threading

app = Flask(__name__)

HTTP_PORT = int(config.HTTP_PORT)

blockchain = Blockchain()
# Using current timestamp as seed for wallet
wallet = Wallet()
transaction_pool = TransactionPool()
p2pserver = P2pServer(blockchain, transaction_pool, wallet)


@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([block.to_json() for block in blockchain.chain])


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transaction_pool.transactions)


@app.route('/transact', methods=['POST'])
def post_transact():
    data = request.json
    to = data['to']
    amount = data['amount']
    type_ = data['type']
    transaction = wallet.create_transaction(
        to, amount, type_, blockchain, transaction_pool)
    p2pserver.broadcast_transaction(transaction)
    return redirect('/transactions')


@app.route('/bootstrap', methods=['GET'])
def bootstrap_system():
    p2pserver.bootstrap_system()
    return jsonify(message="System bootstrapped")


@app.route('/public-key', methods=['GET'])
def get_public_key():
    return jsonify(publicKey=wallet.public_key)


@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balance=blockchain.get_balance(wallet.public_key))


def run_p2pserver():
    print("Running p2p server on port: "+str(config.P2P_PORT))
    p2pserver.listen()


if __name__ == '__main__':
    p2p_thread = threading.Thread(target=run_p2pserver)
    p2p_thread.start()
    app.run(port=HTTP_PORT, debug=False, host="0.0.0.0")
