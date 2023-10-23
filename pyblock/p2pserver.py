import json
import websocket,websocket_server
from websocket import WebSocketApp
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from websocket_server import WebsocketServer
from typing import Type
import pyblock.config as config

P2P_PORT = int(config.P2P_PORT)
PEERS = config.PEERS

MESSAGE_TYPE = {
    'chain': 'CHAIN',
    'block': 'BLOCK',
    'transaction': 'TRANSACTION',
    'clear_transactions': 'CLEAR_TRANSACTIONS'
}


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet]):
        self.blockchain = blockchain
        self.sockets = []
        self.transaction_pool = transaction_pool
        self.wallet = wallet

    def listen(self):
        self.server = WebsocketServer(port=P2P_PORT)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.connect_to_peers()
        self.server.run_forever()
        print(f"Listening for peer-to-peer connections on port: {P2P_PORT}")

    def new_client(self, client, server):
        print("Socket connected:", client['id'])
        self.sockets.append(client)
        self.send_chain(client)

    def client_left(self, client, server):
        print("Client left:", client['id'])
        self.sockets.remove(client)

    def message_received(self, client, server, message):
        data = json.loads(message)
        print("Received data from peer:", data["type"])

        if data["type"] == MESSAGE_TYPE["chain"]:
            self.blockchain.replace_chain(data["chain"])
        elif data["type"] == MESSAGE_TYPE["transaction"]:
            if not self.transaction_pool.transaction_exists(data["transaction"]):
                self.transaction_pool.add_transaction(data["transaction"])
                self.broadcast_transaction(data["transaction"])
                if self.transaction_pool.threshold_reached():
                    if self.blockchain.get_leader() == self.wallet.get_public_key():
                        block = self.blockchain.create_block(
                            self.transaction_pool.transactions, self.wallet)
                        self.broadcast_block(block)
        elif data["type"] == MESSAGE_TYPE["block"]:
            if self.blockchain.is_valid_block(data["block"]):
                self.broadcast_block(data["block"])
                self.transaction_pool.clear()
            # TODO: Add logic to handle invalid block and penalise the validator

    def connect_to_peers(self):
        for peer in PEERS:
            try:
                socket_app = WebSocketApp(peer,
                                                    on_message=self.on_peer_message,
                                                    on_close=self.on_peer_close,
                                                    on_open=self.on_peer_open)
                socket_app.run_forever()
            except Exception as e:
                print(f"Failed to connect to peer {peer}. Error: {e}")

    def on_peer_message(self, ws, message):
        self.message_received(ws, None, message)

    def on_peer_close(self, ws, *args):
        pass

    def on_peer_open(self, ws):
        pass

    def send_chain(self, socket):
        message = json.dumps({
            "type": MESSAGE_TYPE["chain"],
            "chain": self.blockchain.chain
        })
        self.server.send_message(socket, message)

    def sync_chain(self):
        for socket in self.sockets:
            self.send_chain(socket)

    def broadcast_transaction(self, transaction):
        for socket in self.sockets:
            self.send_transaction(socket, transaction)

    def send_transaction(self, socket, transaction):
        message = json.dumps({
            "type": MESSAGE_TYPE["transaction"],
            "transaction": transaction
        })
        self.server.send_message(socket, message)

    def broadcast_block(self, block):
        for socket in self.sockets:
            self.send_block(socket, block)

    def send_block(self, socket, block):
        message = json.dumps({
            "type": MESSAGE_TYPE["block"],
            "block": block
        })
        self.server.send_message(socket, message)

# Bootstrap system..


# if __name__ == "__main__":
#     blockchain = Blockchain()
#     transaction_pool = TransactionPool()
#     wallet = Wallet()
#     p2p_server = P2pServer(blockchain, transaction_pool, wallet)
#     p2p_server.listen()
