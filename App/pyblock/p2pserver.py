import numpy as np
import streamlit as st
import json
import websocket
from pyblock.blockchain.blockchain import Blockchain
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import TransactionPool
from websocket_server import WebsocketServer
from typing import Type
from pyblock.chainutil import *
from pyblock.peers import *
from pyblock.wallet.transaction import *


MESSAGE_TYPE = {
    'chain': 'CHAIN',
    'block': 'BLOCK',
    'transaction': 'TRANSACTION',
    'new_validator': 'NEW_VALIDATOR',
    'vote': 'VOTE',
    "block_proposer_address": "BLOCK_PROPOSER_ADDRESS"
}
# to handle self.... self.message_received(None, None, message)


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet]):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.wallet = wallet  # assuming initialised wallet
        self.accounts = blockchain.accounts
        self.connections = set()
        self.received_block = None
        self.block_received = None
        self.block_proposer = None

    #SEND SIGNED MESSAGE TO GIVEN SOCKET
    def sendEncryptedMessage(self, socket, message):
        self.server.send_message(
            socket, ChainUtil.encryptWithSoftwareKey(message)
        )

    def listen(self):
        print("Starting p2p server...")
        self.create_self_account()
        self.server = WebsocketServer(port=P2P_PORT, host="0.0.0.0")
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.connect_to_peers()
        self.server.account = self.wallet.get_public_key()
        self.server.run_forever()
        
    #CREATE A NEW ACCOUNT FOR OWN-USER
    def create_self_account(self):
        self.accounts.addANewClient(
            address=self.wallet.get_public_key(), clientPort = None
        )

        print("ACCOUNT CREATED")

    #FUNCTION CALLED WHEN A NEW CLIENT JOINS SERVER
    def new_client(self, client, server):
        print("Socket connected:", client)
        
        #ADD CLIENT TO CONNECTIONS
        self.connections.add(client)
        self.send_chain(client)
        self.send_mempool(client)
        self.send_current_block_proposer(client)
        
    #SEND THE CURRENT BLOCK PROPOSER TO A NEWLY JOINED NODE
    def send_current_block_proposer(self, socket):
        message = json.dumps({
            "type": MESSAGE_TYPE["block_proposer_address"],
            "address": st.session_state.p2pserver.block_proposer
        })

        self.sendEncryptedMessage(socket, message)
        
        
    #FUNCTION CALLED WHEN A CLIENT LEAVES SERVER
    def client_left(self, client, server):
        print("Client left:", client['id'])
        
        #REMOVE CLIENT FROM CONNECTIONS
        self.connections.remove(client)
        # self.accounts.clientLeft(clientport=client)

    #FUNCTION CALLED WHEN A MESSAGE IS RECIEVED FROM ANOTHER CLIENT
    def message_received(self, client, server, message):
        
        try:
            #CONVERT FROM JSON TO DICTIONARY
            data = json.loads(message)

        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return
        
        #CHECK IF SIGNATURE IS VALID
        if not ChainUtil.decryptWithSoftwareKey(data):
            print("Invalid message recieved.")
            return

        print("MESSAGE RECIEVED OF TYPE", data["type"])

        #IF BLOCKCAIN RECIEVED
        if data["type"] == MESSAGE_TYPE["chain"]:
            #TRY TO REPLACE IF LONGER CHAIN
            self.blockchain.replace_chain(data["chain"])

        
        elif data["type"] == MESSAGE_TYPE["transaction"]:
            #CREATE TRANSACTION FROM JSON FORM
            transaction = Transaction.from_json(data["transaction"])
            
            #IF DOESN'T EXIST; ADD IT [VALIDATED AT TIME OF BLOCK RECIEVED]
            self.transaction_pool.add_transaction(transaction)
            
            #ADD TO TRANSACTIONS SENT BY A USER TO VIEW
            self.accounts.add_transaction(transaction)



        elif data["type"] == MESSAGE_TYPE["block"]:
            # CHECK BLOCK IS PROPOSED BY CURRENT BLOCK PROPOSER
            if self.block_proposer != data["block"].validator:
                return
            #CHECK VALIDITY OF BLOCK & ITS TRANSACTIONS
            if (self.blockchain.is_valid_block(
                data["block"], self.transaction_pool, self.accounts)):
                
                # SET RECIEVED FLAG TO ALLOW VOTING
                self.block_received = True
                self.received_block = data["block"]

        elif data["type"] == MESSAGE_TYPE["new_validator"]:
            # NEW VALIDATOR
            new_validator_public_key = data["public_key"]
            new_validator_stake = data["stake"]
            
            # CHECK & MAKE THE ACCOUNT A VALIDATOR
            self.accounts.makeAccountValidatorNode(
                address=new_validator_public_key, stake=new_validator_stake
            )

        # TODO: HOW WILL A NEW NODE SEND MESSAGE TO OTHER CLIENTS?
        elif data["type"] == MESSAGE_TYPE["new_node"]:
            
            public_key = data["public_key"]
            self.accounts.addANewClient(address=public_key, clientPort=client)
            self.send_mempool(client)
            self.send_chain(client)
            
        elif data["type"] == MESSAGE_TYPE["vote"]:
            self.handle_votes(data)
            
        elif data["type"] == MESSAGE_TYPE["block_proposer_address"]:
            #SET THE CURRENT BLOCK PROPOSER ACC. TO MESSAGE
            self.block_proposer = data["address"]
            
        
    

    def send_mempool(self, socket):
        transaction_list = list(
            self.transaction_pool.transactions
        )
        
        message = json.dumps({
            "type": MESSAGE_TYPE["chain"],
            "chain": transaction_list
        })
        
        self.sendEncryptedMessage(socket, message)
        
    def handle_votes(self, data):
        # CHECK IF THE VOTE IS VALID
        if not self.accounts.check_if_active(data["address"]):
            print("INVALID VOTE")
            return
        
        # IF NOT CURRENT BLOCK
        if data["block_index"] != st.session_state.p2pserver.received_block.index:
            print("OLD VOTE RECEIVED")
            return

        # INCREMENT NUMBER OF VOTES FOR THE BLOCK
        self.received_block.votes.add(data["address"])

        # INCREMENT VOTES FOR THE TRANSACTIONS
        transactions_dict = {
            transaction.id: transaction for transaction in st.session_state.p2pserver.received_block.transactions
        }
        
        for key, value in self.received_block.transactions:
            if value == "True":
                transactions_dict[key].positive_votes += 1

        # JUST IN CASE OF PASS BY VALUE
        for index, transaction in enumerate(st.session_state.p2pserver.received_block.transactions):
            self.received_block.transactions[index] = transactions_dict[transaction.id]

    def broadcast_new_node(self):
        """
        Broadcast new node's public key to all to create a new account
        """
        
        # active_accounts = self.accounts.get_active_accounts()
        for client in self.connections:
            self.send_new_node(
                client, self.wallet.get_public_key()
            )

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
        
        message = ChainUtil.encryptWithSoftwareKey(message)

        message = json.dumps(message, cls=CustomJSONEncoder)
        
        self.message_received(None, None, message)
        
        
        print("ACTIVE ACCOUNTS: ", self.connections)
        for client in self.connections:
            self.send_new_validator(
                client, self.wallet.get_public_key(), stake)

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
        self.send_new_node(
            ws, self.wallet.get_public_key()
        )

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
        # active_accounts = self.accounts.get_active_accounts(
        # self.wallet.get_public_key())
        for client in  self.connections:
            #Assuming the account's clientPort can be used to send messages
            # and there's a method in P2pServer to get the socket by its client port
            # socket = self.get_socket_by_client_port(account.clientPort)
            # if socket:
            self.send_chain(client)

    def broadcast_transaction(self, transaction):
        message = {
            "type": MESSAGE_TYPE["transaction"],
            "transaction": transaction.to_json()
        }
        
        message = ChainUtil.encryptWithSoftwareKey(message)
        
        message = json.dumps(message, cls = CustomJSONEncoder)
        
        print("MESSAGE SENT TO SELF")
        
        self.message_received(
            None, None, message
        )
        
        print("ACTIVE ACCOUNTS: ", self.connections)

        for client in self.connections:
            self.send_transaction(
                client, message
            )

    def send_transaction(self, socket, message):
        self.sendEncryptedMessage(socket, message)

    def broadcast_block(self, block):
        message_data = {
            "type": MESSAGE_TYPE["block"],
            "block": block
        }
        
        message = ChainUtil.encryptWithSoftwareKey(message_data)

        message = json.dumps(message, cls=CustomJSONEncoder)
        
        self.message_received(None, None, message)
        
        for client in self.connections:
            self.send_block(client, message_data)

    def broadcast_votes(self, votes_dict):
        votes_list = [(key, value) for key, value in votes_dict.items()]

        # Prepare the message content without the signature
        message_content = {
            "type": MESSAGE_TYPE["vote"],
            "address": self.wallet.get_public_key(),
            "votes": votes_list,
            "block_index": st.session_state.p2pserver.received_block.index
        }

        # # Convert the message content to a JSON string
        message_json = json.dumps(message_content)

        # Sign the JSON string
        signature = self.wallet.sign(message_json)

        # Append the signature to the message content
        message_content['signature'] = signature

        # Convert the full message with signature to JSON
        message = json.dumps(message_content, cls=CustomJSONEncoder)
        

        self.message_received(None, None, message)
        
        for client in self.connections:
            self.sendEncryptedMessage(client, message)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.hex()
        elif isinstance(o, np.float32):
            return float(o)
        return json.JSONEncoder.default(self, o)
