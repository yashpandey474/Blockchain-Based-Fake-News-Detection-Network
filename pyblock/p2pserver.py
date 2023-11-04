import json
import websocket
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from websocket_server import WebsocketServer
from typing import Type
import pyblock.config as config
import pyblock.chainutil as ChainUtil
from pyblock.blockchain.account import Accounts
from pyblock.blockchain.account import Account
P2P_PORT = int(config.P2P_PORT)
PEERS = config.PEERS

MESSAGE_TYPE = {
    'chain': 'CHAIN',
    'block': 'BLOCK',
    'transaction': 'TRANSACTION',
    'clear_transactions': 'CLEAR_TRANSACTIONS',
    'new_validator': 'NEW_VALIDATOR',
    'login': 'LOGIN',
    'challenge': 'CHALLENGE',
    'challenge_response': 'CHALLENGE_RESPONSE'
}


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet], accounts: Type[Accounts]):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.wallet = wallet  # assuming initialised wallet
        self.accounts = accounts

    def sendEncryptedMessage(self, socket, message):
        self.server.send_message(
            socket, ChainUtil.encryptWithSoftwareKey(message))

    def listen(self):
        print("Starting p2p server...")
        self.server = WebsocketServer(port=P2P_PORT, host="0.0.0.0")
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.connect_to_peers()
        self.server.run_forever()

    def new_client(self, client, server):
        print("Socket connected:", client['id'])
        self.send_chain(client)

    def client_left(self, client, server):
        print(client)
        print("Client left:", client['id'])
        self.accounts.clientLeft(clientport=client)

    def message_received(self, client, server, message):
        # Assuming that the incoming message is encrypted and then base64-encoded
        decrypted_message = ChainUtil.decryptWithSoftwareKey(message)

        # Now, attempt to deserialize the decrypted message from JSON
        try:
            data = json.loads(decrypted_message)
        except json.JSONDecodeError:
            print("Failed to decode JSON from decrypted message")
            return

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
        elif data["type"] == MESSAGE_TYPE["new_validator"]:
            # Assuming the new validator sends their public key with this message
            new_validator_public_key = data["public_key"]
            new_validator_stake = data["stake"]
            self.accounts.makeAccountValidatorNode(
                address=new_validator_public_key, stake=new_validator_stake)

        elif data["type"] == MESSAGE_TYPE["new_node"]:
            public_key = data["public_key"]
            self.accounts.addANewClient(address=public_key, clientPort=client)

    # def initialize_wallet(self, public_key: str, private_key: str):
    #     # """
    #     # Initialize the wallet with a public key and a private key.
    #     # """
    #     self.wallet.initialize(public_key, private_key)
    #     self.broadcast_new_validator(public_key)

    def broadcast_new_validator(self, stake):
        """
        Broadcast the new validator's public key to all connected nodes.
        """
        # try:
        # self.accounts.makeAccountValidatorNode(address=self.wallet.get_public_key(),stake=stake)
        # TODO: check if self message works
        active_accounts = self.accounts.get_active_accounts()
        for address in active_accounts:
            self.send_new_validator(
                active_accounts[address].clientPort, self.wallet.get_public_key(), stake)
        # except:
        #     return False

    def send_new_validator(self, socket, public_key: str, stake):
        """
        Send a new validator's public key to the specified socket.
        """
        message = json.dumps({
            "type": MESSAGE_TYPE["new_validator"],
            "public_key": public_key,
            "stake": stake
        })
        self.sendEncryptedMessage(socket, message)

    # def handle_challenge(self,validator_socket, message):
    #     """
    #     Handle a received challenge message.
    #     """
    #     public_key = message['public_key']
    #     challenge = message['challenge']
    #     signature = self.wallet.sign(challenge)

    #     # Send the signature back as a response to the challenge
    #     message = json.dumps({
    #         "type": "CHALLENGE_RESPONSE",
    #         "public_key": public_key,
    #         "signature": signature
    #     })
    #     self.sendEncryptedMessage(validator_socket, message)

    def connect_to_peers(self):
        for peer in PEERS:
            try:
                socket_app = websocket.WebSocketApp(peer,
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
        self.send_new_node(ws, self.wallet.public_key)

    def send_new_node(self, ws, public_key: str):
        """
        Send a new node message with the public key to the specified socket.
        """
        message = json.dumps({
            "type": MESSAGE_TYPE["new_node"],
            "public_key": public_key
        })
        ws.send(message)

    def send_chain(self, socket):
        chain_as_json = [block.to_json() for block in self.blockchain.chain]
        message = json.dumps({
            "type": MESSAGE_TYPE["chain"],
            "chain": chain_as_json
        })
        self.sendEncryptedMessage(socket, message)

    def sync_chain(self):
        active_accounts = self.accounts.get_active_accounts()
        for address, account in active_accounts.items():
            # Assuming the account's clientPort can be used to send messages
            # and there's a method in P2pServer to get the socket by its client port
            socket = self.get_socket_by_client_port(account.clientPort)
            if socket:
                self.send_chain(socket)

    def broadcast_transaction(self, transaction):
        active_accounts = self.accounts.get_active_accounts()
        for address in active_accounts:
            self.send_transaction(
                active_accounts[address].clientPort, transaction)

    def send_transaction(self, socket, transaction):
        message = json.dumps({
            "type": MESSAGE_TYPE["transaction"],
            "transaction": transaction
        })
        self.sendEncryptedMessage(socket, message)

    def broadcast_block(self, block):
        active_accounts = self.accounts.get_active_accounts()
        for address in active_accounts:
            self.send_block(active_accounts[address].clientPort, block)

    def send_block(self, socket, block):
        message = json.dumps({
            "type": MESSAGE_TYPE["block"],
            "block": block
        })
        self.sendEncryptedMessage(socket, message)

# if __name__ == "__main__":
#     blockchain = Blockchain()
#     transaction_pool = TransactionPool()
#     wallet = Wallet()
#     p2p_server = P2pServer(blockchain, transaction_pool, wallet)
#     p2p_server.listen()
