from flask import Flask, request, jsonify, redirect
import time,os
from blockchain.blockchain import Blockchain
from ..wallet.wallet import Wallet
from ..wallet.transaction_pool import TransactionPool
from p2pserver import P2pServer

app = Flask(__name__)

HTTP_PORT = int(os.environ.get('HTTP_PORT', 3001))

blockchain = Blockchain()
wallet = Wallet(str(int(time.time())))  # Using current timestamp as seed for wallet
transaction_pool = TransactionPool()
p2pserver = P2pServer(blockchain, transaction_pool, wallet)


@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify(blockchain.chain)


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transaction_pool.transactions)


@app.route('/transact', methods=['POST'])
def post_transact():
    data = request.json
    to = data['to']
    amount = data['amount']
    type_ = data['type']
    transaction = wallet.create_transaction(to, amount, type_, blockchain, transaction_pool)
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


if __name__ == '__main__':
    app.run(port=HTTP_PORT, debug=True)
    p2pserver.listen()
