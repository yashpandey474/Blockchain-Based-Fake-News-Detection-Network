from flask import Flask, jsonify, request
# Assuming you have the Blockchain, P2pServer, Wallet, and TransactionPool modules translated to Python already
from ..blockchain.blockchain import Blockchain
from ..app.p2pserver import P2pServer
from ..wallet.wallet import Wallet
from ..wallet.transaction_pool import TransactionPool
from config import TRANSACTION_THRESHOLD

HTTP_PORT = 3000

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet("i am the first leader")
transactionPool = TransactionPool()
p2pserver = P2pServer(blockchain, transactionPool, wallet)

@app.route("/ico/transactions", methods=["GET"])
def get_transactions():
    return jsonify(transactionPool.transactions)

@app.route("/ico/blocks", methods=["GET"])
def get_blocks():
    return jsonify(blockchain.chain)

@app.route("/ico/transact", methods=["POST"])
def post_transact():
    data = request.json
    to = data.get("to")
    amount = data.get("amount")
    type_ = data.get("type")
    transaction = wallet.createTransaction(to, amount, type_, blockchain, transactionPool)
    p2pserver.broadcastTransaction(transaction)
    if len(transactionPool.transactions) >= TRANSACTION_THRESHOLD:
        block = blockchain.createBlock(transactionPool.transactions, wallet)
        p2pserver.broadcastBlock(block)
    return jsonify(transactionPool.transactions), 201

@app.route("/ico/public-key", methods=["GET"])
def get_public_key():
    return jsonify(publicKey=wallet.publicKey)

@app.route("/ico/balance", methods=["GET"])
def get_balance():
    return jsonify(balance=blockchain.getBalance(wallet.publicKey))

@app.route("/ico/balance-of", methods=["POST"])
def post_balance_of():
    data = request.json
    public_key = data.get("publicKey")
    return jsonify(balance=blockchain.getBalance(public_key))

if __name__ == "__main__":
    app.run(port=HTTP_PORT, debug=True)
    p2pserver.listen()
