import numpy as np
import streamlit as st
import json
import websocket
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from websocket_server import WebsocketServer
from typing import Type
import pyblock.config as config
from pyblock.chainutil import *
from pyblock.peers import *
from pyblock.blockchain.account import Accounts
from pyblock.blockchain.account import Account


MESSAGE_TYPE = {
    'chain': 'CHAIN',
    'block': 'BLOCK',
    'transaction': 'TRANSACTION',
    'clear_transactions': 'CLEAR_TRANSACTIONS',
    'new_validator': 'NEW_VALIDATOR',
    'login': 'LOGIN',
    'challenge': 'CHALLENGE',
    'challenge_response': 'CHALLENGE_RESPONSE',
    'vote': 'VOTE',
}


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet]):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.wallet = wallet  # assuming initialised wallet
        self.accounts = blockchain.accounts

    def sendEncryptedMessage(self, socket, message):
        self.server.send_message(
            socket, ChainUtil.encryptWithSoftwareKey(message))

    def listen(self):
        print("Starting p2p server...")
        self.create_self_account()
        self.server = WebsocketServer(port=P2P_PORT, host="0.0.0.0")
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.connect_to_peers()
        self.server.run_forever()

    def create_self_account(self):
        self.accounts.addANewClient(
            address=self.wallet.public_key, clientPort=None)

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

        print("MESSAGE RECIEVED OF TYPE", data["type"])

        if data["type"] == MESSAGE_TYPE["chain"]:
            if len(data["chain"]) > len(self.blockchain.chain):
                self.blockchain.replace_chain(data["chain"])

        elif data["type"] == MESSAGE_TYPE["transaction"]:
            if not self.transaction_pool.transaction_exists(data["transaction"]):
                self.transaction_pool.add_transaction(data["transaction"])
                # self.broadcast_transaction(data["transaction"])
                # if self.transaction_pool.threshold_reached():
                #     if self.blockchain.get_leader() == self.wallet.get_public_key():
                #         block = self.blockchain.create_block(
                #             self.transaction_pool.transactions, self.wallet)
                #         self.broadcast_block(block)

        elif data["type"] == MESSAGE_TYPE["block"]:
            if self.blockchain.is_valid_block(data["block"]):
                # self.broadcast_block(data["block"])

                # #REMOVE INCLUDED TRANSACTIONS FROM THE MEMPOOL
                # self.transaction_pool.remove(data["block"].data)

                # VOTE ON THE TRANSACTIONS
                st.session_state.block_recieved = True
                st.session_state.recieved_block = data["block"]

        elif data["type"] == MESSAGE_TYPE["new_validator"]:
            # Assuming the new validator sends their public key with this message
            new_validator_public_key = data["public_key"]
            new_validator_stake = data["stake"]
            self.accounts.makeAccountValidatorNode(
                address=new_validator_public_key, stake=new_validator_stake)

        elif data["type"] == MESSAGE_TYPE["new_node"]:
            public_key = data["public_key"]
            self.accounts.addANewClient(address=public_key, clientPort=client)

        elif data["type"] == MESSAGE_TYPE["vote"]:
            self.handle_votes(data)

    def handle_votes(self, data):
        # TODO: Implement THIS
        '''"address": self.wallet.get_public_key(),
            "votes": votes_list,
            "block_index": st.session_state.received_block.index'''
        # CHECK IF THE VOTE IS VALID
        if not self.accounts.check_if_active(data["address"]):
            print("INVALID VOTE")
            return
        # IF NOT CURRENT BLOCK
        if data["block_index"] != st.session_state.received_block.index:
            print("OLD VOTE RECEIVED")
            return

        # INCREMENT NUMBER OF VOTES FOR THE BLOCK
        st.session_state.received_block.votes += 1

        # INCREMENT VOTES FOR THE TRANSACTIONS
        transactions_dict = {
            transaction.id: transaction for transaction in st.session_state.received_block.transactions}
        for key, value in st.session_state.received_block.transactions:
            if value == "True":
                transactions_dict[key].positive_votes += 1

        # JUST IN CASE OF PASS BY VALUE
        for index, transaction in enumerate(st.session_state.received_block.transactions):
            st.session_state.received_block.transactions[index] = transactions_dict[transaction.id]

    def broadcast_new_node(self):
        """
        Broadcast new node's public key to all to create a new account
        """
        active_accounts = self.accounts.get_active_accounts()
        for address in active_accounts:
            self.send_new_node(
                active_accounts[address].clientPort, self.wallet.get_public_key()
            )

    def broadcast_new_validator(self, stake):
        """
        Broadcast the new validator's public key to all connected nodes.
        """
        # try:
        # self.accounts.makeAccountValidatorNode(address=self.wallet.get_public_key(),stake=stake)
        # TODO: check if self message works
        active_accounts = self.accounts.get_active_accounts()
        print("ACTIVE ACCOUNTS: ", active_accounts)
        for address in active_accounts:
            self.send_new_validator(
                active_accounts[address].clientPort, self.wallet.get_public_key(), stake)

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
        print("ACTIVE ACCOUNTS: ", active_accounts)
        for address in active_accounts:
            self.send_transaction(
                active_accounts[address].clientPort, transaction)

    def send_transaction(self, socket, transaction):
        message = json.dumps({
            "type": MESSAGE_TYPE["transaction"],
            "transaction": transaction.to_json()
        }, cls=CustomJSONEncoder)
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

    def broadcast_votes(self, votes_dict):
        # Create a list of votes with id and corresponding boolean value as integer
        votes_list = [(key, value) for key, value in votes_dict.items()]

        # Prepare the message content without the signature
        message_content = {
            "type": MESSAGE_TYPE["vote"],
            "address": self.wallet.get_public_key(),
            "votes": votes_list,
            "block_index": st.session_state.received_block.index
        }

        # Convert the message content to a JSON string
        message_json = json.dumps(message_content)

        # Sign the JSON string
        signature = self.wallet.sign(message_json)

        # Append the signature to the message content
        message_content['signature'] = signature

        # APPEND THE BLOCK NUMBER

        # Convert the full message with signature to JSON
        message = json.dumps(message_content)

        # Broadcast the message to all active accounts
        active_accounts = self.accounts.get_active_accounts()
        for address in active_accounts:
            client_socket = active_accounts[address].clientPort
            self.sendEncryptedMessage(client_socket, message)


# if __name__ == "__main__":
#     blockchain = Blockchain()
#     transaction_pool = TransactionPool()
#     wallet = Wallet()
#     p2p_server = P2pServer(blockchain, transaction_pool, wallet)
#     p2p_server.listen()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.hex()
        elif isinstance(o, np.float32):
            return float(o)
        return json.JSONEncoder.default(self, o)
