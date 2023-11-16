import numpy as np
import streamlit as st
import json
import websocket
from pyblock.blockchain.blockchain import Blockchain
from pyblock.blockchain.block import *
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from websocket_server import WebsocketServer
from typing import Type
from pyblock.chainutil import *
from pyblock.peers import *
from pyblock.wallet.transaction import *
from pyblock.blockchain.account import *

import streamlit as st
import requests
import zmq
import logging
import threading
import socket
import queue
import random as random

MESSAGE_TYPE = {
    'chain': 'CHAIN',
    'block': 'BLOCK',
    'transaction': 'TRANSACTION',
    'new_validator': 'NEW_VALIDATOR',
    'vote': 'VOTE',
    "block_proposer_address": "BLOCK_PROPOSER_ADDRESS",
    "new_node": "NEW_NODE"
}
# to handle self.... self.message_received(None, None, message)
logging.basicConfig(level=logging.INFO)
# Configuration
server_url = 'http://65.1.130.255/app'  # Local server URL
send_timeout = 500
receive_timeout = 500

context = zmq.Context()
myClientPort = 0


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet], user_type="Reader"):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.wallet = wallet  # assuming initialised wallet
        self.accounts = blockchain.accounts
        self.user_type = user_type
        self.connections = set()
        self.received_block = None
        self.block_received = None
        self.block_proposer = None
        self.peers = []

    def private_send_message(self, clientPort, message):
        reply = None
        # assumes message is encrypted
        zmq_socket = context.socket(zmq.REQ)
        # Receive timeout in milliseconds
        zmq_socket.setsockopt(zmq.RCVTIMEO, receive_timeout)
        # Send timeout in milliseconds
        zmq_socket.setsockopt(zmq.SNDTIMEO, send_timeout)
        try:
            tcpaddr = f"tcp://{clientPort}"
            print(f"Sending message to {tcpaddr}")
            zmq_socket.connect(tcpaddr)
            zmq_socket.send_string(message)
            reply = zmq_socket.recv_string()
            print(f"Received reply from {clientPort}: {reply}")
        except Exception as e:
            # if e.errno == zmq.ETIMEDOUT:
            #     print("TIMED OUT\n")
            logging.error(f"Error communicating with {clientPort}: {e}")
        finally:
            zmq_socket.close()
        return reply

    def get_encrypted_message(self, message):
        message['clientPort'] = myClientPort  # Add the clientPort
        encrypted_message = ChainUtil.encryptWithSoftwareKey(
            message)  # Re-encode and encrypt
        return encrypted_message

    def register(self, public_key, clientPort):
        print("Registering with public key and address")
        data = {'public_key': public_key, 'address': clientPort}
        try:
            response = requests.post(f'{server_url}/register', json=data)
            print(f"Response from server: {response}")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Registration failed: {e}")
            return None

    def get_ip_address(self):
        print("Getting IP address")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
                print(f"Obtained IP address: {ip_address}")
                return ip_address
        except Exception as e:
            logging.error(f"Error obtaining IP address: {e}")
            return None

    def start_server(self):
        port = random.randint(50000, 65535)
        print(f"Starting server on port {port}")
        
        ip_address = self.get_ip_address()
        if ip_address is None:
            print("Failed to obtain IP address. Server cannot start.")
            return
        
        global myClientPort
        myClientPort = f"{ip_address}:{port}"
        zmq_socket = context.socket(zmq.REP)
        zmq_socket.bind(f"tcp://{myClientPort}")

        self.register(clientPort=f"{ip_address}:{port}",
                      public_key=self.wallet.get_public_key())
        
        print("Creating new thread")
        thread = threading.Thread(target=self.broadcast_new_node)
        thread.start()
        
        print("New thread started")
        while True:
            message = zmq_socket.recv_string()
            print(f"Received message: {message}")
            zmq_socket.send_string(
                f"Successfully received message {message}. Sent from {myClientPort}")
            self.message_received(message)

    def broadcast_message(self, message):
        print("Broadcasting message")
        responses = []
        newpeers = self.get_peers()
        encrypted_message = self.get_encrypted_message(message)
        print(f"Peers: {newpeers}")
        for peer in newpeers:
            responses.append(self.private_send_message(
                peer['address'], encrypted_message))
        return responses

    def send_direct_encrypted_message(self, message, clientPort):
        print("Sending direct message")
        encrypted_message = self.get_encrypted_message(message)
        return self.private_send_message(clientPort, encrypted_message)

    def get_peers(self):
        print("Fetching peers")
        global peers

        try:
            response = requests.get(f'{server_url}/peers')
            response.raise_for_status()
            peers_list = response.json()
            print(f"Received peers: {peers_list}")
            self.peers = peers_list
            return peers_list

        except requests.RequestException as e:
            logging.error(f"Failed to fetch peers: {e}")
            print('Failed to fetch peers')
            return []

    def listen(self):
        print("Starting tcp server...")
        server_thread = threading.Thread(
            target=self.start_server, daemon=True)
        server_thread.start()
        print("Server thread started")

    # # FUNCTION CALLED WHEN A NEW CLIENT JOINS SERVER
    # def new_client(self, client, server):
    #     print("Socket connected:", client)

    #     # ADD CLIENT TO CONNECTIONS
    #     self.connections.add(client)
    #     self.send_chain(client)
    #     self.send_mempool(client)
    #     self.send_current_block_proposer(client)

    # SEND THE CURRENT BLOCK PROPOSER TO A NEWLY JOINED NODE

    def send_current_block_proposer(self, clientPort):
        message = {
            "type": MESSAGE_TYPE["block_proposer_address"],
            "address": self.block_proposer
        }

        self.send_direct_encrypted_message(message, clientPort)

    # FUNCTION CALLED WHEN A CLIENT LEAVES SERVER

    # def client_left(self, client, server):
    #     print("Client left:", client['id'])

    #     # REMOVE CLIENT FROM CONNECTIONS
    #     self.connections.remove(client)
    #     # self.accounts.clientLeft(clientport=client)

    # FUNCTION CALLED WHEN A MESSAGE IS RECIEVED FROM ANOTHER CLIENT
    def message_received(self, message):
        try:
            # CONVERT FROM JSON TO DICTIONARY
            data = json.loads(message)

        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return

        # CHECK IF SIGNATURE IS VALID
        if not ChainUtil.decryptWithSoftwareKey(data):
            print("Invalid message recieved.")
            return

        clientPort = data["clientPort"]

        print("MESSAGE RECIEVED OF TYPE", data["type"])

        # IF BLOCKCAIN RECIEVED
        if data["type"] == MESSAGE_TYPE["chain"]:
            # TRY TO REPLACE IF LONGER CHAIN
            self.blockchain.replace_chain(data["chain"])
            # TODO: SUS
            print("REPLACED CHAIN")
            self.accounts.from_json(json_data=data["accounts"])
            print("REPLACED ACCOUNTS")
            print(self.accounts.accounts)
            self.transaction_pool.from_json(
                json_data=data["transaction_pool"])
            print("REPLACED TRANSACTION POOL")
            print(self.transaction_pool)

        elif data["type"] == MESSAGE_TYPE["transaction"]:
            # CREATE TRANSACTION FROM JSON FORM
            transaction = Transaction.from_json(data["transaction"])

            # IF DOESN'T EXIST; ADD IT [VALIDATED AT TIME OF BLOCK RECIEVED]
            self.transaction_pool.add_transaction(transaction)

            # ADD TO TRANSACTIONS SENT BY A USER TO VIEW
            self.accounts.add_transaction(transaction)

        elif data["type"] == MESSAGE_TYPE["block"]:
            # CHECK BLOCK IS PROPOSED BY CURRENT BLOCK PROPOSER
            block = Block.from_json(data["block"])

            print(block.transactions)
            if self.block_proposer != block.validator:
                print("RECEIVED BLOCK DOESN'T HAVE CORRECT VALIDATOR!")
                return

            # CHECK VALIDITY OF BLOCK & ITS TRANSACTIONS
            if (self.blockchain.is_valid_block(
                    block, self.transaction_pool, self.accounts)):

                # SET RECIEVED FLAG TO ALLOW VOTING
                self.block_received = True
                self.received_block = block
                self.accounts.add_sent_block(block.validator, block)

            else:
                print("RECEIVED BLOCK DEEMED INVALID.")

        elif data["type"] == MESSAGE_TYPE["new_validator"]:
            # NEW VALIDATOR
            new_validator_public_key = data["public_key"]
            new_validator_stake = data["stake"]

            # CHECK & MAKE THE ACCOUNT A VALIDATOR
            self.accounts.makeAccountValidatorNode(
                address=new_validator_public_key, stake=new_validator_stake
            )

        elif data["type"] == MESSAGE_TYPE["new_node"]:
            clientPort = data["clientPort"]
            self.accounts.addANewClient(
                address=data["public_key"], clientPort=clientPort, userType=self.user_type)
            if (clientPort != myClientPort):
                self.send_chain(clientPort)
                self.send_current_block_proposer(clientPort)

        elif data["type"] == MESSAGE_TYPE["vote"]:
            self.handle_votes(data)

        elif data["type"] == MESSAGE_TYPE["block_proposer_address"]:
            # SET THE CURRENT BLOCK PROPOSER ACC. TO MESSAGE
            self.block_proposer = data["address"]

    def handle_votes(self, data):
        # CHECK IF THE VOTE IS VALID
        if not self.accounts.check_if_active(data["address"]):
            print("INVALID VOTE")
            return

        # IF NOT CURRENT BLOCK
        if data["block_index"] != self.received_block.index:
            print("OLD VOTE RECEIVED")
            return

        # INCREMENT NUMBER OF VOTES FOR THE BLOCK
        self.received_block.votes.add(data["address"])

        # INCREMENT VOTES FOR THE TRANSACTIONS
        transactions_dict = {
            transaction.id: transaction for transaction in self.received_block.transactions
        }

        for key, value in self.received_block.transactions:
            if value == "True":
                transactions_dict[key].positive_votes.add(data["address"])
            else:
                transactions_dict[key].negative_votes.add(data["address"])

        # JUST IN CASE OF PASS BY VALUE
        for index, transaction in enumerate(self.received_block.transactions):
            self.received_block.transactions[index] = transactions_dict[transaction.id]

    def broadcast_new_validator(self, stake):
        """
        Broadcast the new validator's public key to all connected nodes.
        """
        # try:
        # self.accounts.makeAccountValidatorNode(address=self.wallet.get_public_key(),stake=stake)
        # TODO: check if self message works
        message = {
            "type": MESSAGE_TYPE["new_validator"],
            "public_key": self.wallet.get_public_key(),
            "stake": stake
        }

        self.broadcast_message(message)

    def send_new_validator(self, clientPort, public_key: str, stake):
        """
        Send a new validator's public key to the specified socket.
        """
        message = {
            "type": MESSAGE_TYPE["new_validator"],
            "public_key": public_key,
            "stake": stake
        }

        self.send_direct_encrypted_message(message, clientPort=clientPort)

    def broadcast_new_node(self):
        """
        Broadcast a new node message.
        """
        message = {
            "type": MESSAGE_TYPE["new_node"],
            "public_key": self.wallet.get_public_key(),
            "clientPort": myClientPort
        }
        self.broadcast_message(message)

    def send_chain(self, clientPort):
        chain_as_json = [block.to_json() for block in self.blockchain.chain]
        message = {
            "type": MESSAGE_TYPE["chain"],
            "chain": chain_as_json,
            "accounts": self.accounts.to_json(),
            "transaction_pool": TransactionPool.to_json(self.transaction_pool)
        }
        self.send_direct_encrypted_message(
            message=message, clientPort=clientPort)

    def broadcast_transaction(self, transaction):
        message = {
            "type": MESSAGE_TYPE["transaction"],
            "transaction": transaction.to_json()
        }
        self.broadcast_message(message)

    def broadcast_block(self, block):
        message = {
            "type": MESSAGE_TYPE["block"],
            "block": block.to_json()
        }
        self.broadcast_message(message)

    def broadcast_votes(self, votes_dict):
        votes_list = [(key, value) for key, value in votes_dict.items()]

        # Prepare the message content without the signature
        message_content = {
            "type": MESSAGE_TYPE["vote"],
            "address": self.wallet.get_public_key(),
            "votes": votes_list,
            "block_index": self.received_block.index
        }

        # # Convert the message content to a JSON string
        message_json = json.dumps(message_content, cls=CustomJSONEncoder)

        # Sign the JSON string
        signature = self.wallet.sign(message_json)

        # Append the signature to the message content
        message_content['signature'] = signature

        # Convert the full message with signature to JSON

        # self.message_received(None, None, message)

        self.broadcast_message(message_content)
