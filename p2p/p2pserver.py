import json
from blockchain.blockchain import Blockchain
from blockchain.block import *
from wallet.wallet import Wallet
from wallet.transaction_pool import TransactionPool
from typing import Type
from extra.chainutil import *
from wallet.transaction import *
from blockchain.account import *
from .heartbeat_manager import *
import requests
import zmq
import logging
import threading
import socket
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

logging.basicConfig(level=logging.INFO)
server_url = 'https://ujjwalaggarwal.pythonanywhere.com/app'  # Local server URL
send_timeout = 5000
receive_timeout = 5000
heartbeat_timeout = 30


def printy(*args):
    joined_string = ' '.join(str(arg) for arg in args)
    try:
        print(f"\033[93m{joined_string}\033[00m")
    except:
        print(joined_string)


class P2pServer:
    def __init__(self, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool], wallet: Type[Wallet], user_type="Reader"):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.wallet = wallet  # assuming initialised wallet
        self.accounts = blockchain.accounts
        self.user_type = user_type
        self.received_block = None
        self.block_received = None
        self.block_proposer = None
        self.peers = {}
        self.myClientPort = 0
        self.context = zmq.Context()
        self.heartbeat_manager = None
        self.exited_flag = False

        # IF THE P2PSERVER HAS RECEIVED CURRENT TRANSACTION POOL & CHAIN ETC.
        self.initialised = False

    def private_send_message(self, clientPort, message):
        reply = None
        # assumes message is encrypted
        zmq_socket = self.context.socket(zmq.REQ)
        # Receive timeout in milliseconds
        zmq_socket.setsockopt(zmq.RCVTIMEO, receive_timeout)
        # Send timeout in milliseconds
        zmq_socket.setsockopt(zmq.SNDTIMEO, send_timeout)
        try:
            tcpaddr = f"tcp://{clientPort}"
            printy(f"Sending message to {tcpaddr}")
            zmq_socket.connect(tcpaddr)
            zmq_socket.send_string(message)
            reply = zmq_socket.recv_string()
            printy(f"Received reply from {clientPort}: {reply}")

        except Exception as e:
            reply = f"Failed to send message {message} to {clientPort}: {e}"
        finally:
            zmq_socket.close()
        return reply

    def get_encrypted_message(self, message):
        message['clientPort'] = self.myClientPort  # Add the clientPort
        encrypted_message = ChainUtil.encryptWithSoftwareKey(
            message)  # Re-encode and encrypt
        return encrypted_message

    def register(self, public_key, clientPort):
        printy("Registering with public key and address")
        data = {'public_key': public_key, 'address': clientPort}
        try:
            response = requests.post(f'{server_url}/register', json=data)
            printy(f"Register api. Response from server: {response}")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Registration failed: {e}")
            return None

    def get_ip_address(self):
        printy("Getting IP address")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
                printy(f"Obtained IP address: {ip_address}")
                return ip_address
        except Exception as e:
            logging.error(f"Error obtaining IP address: {e}")
            return None

    def is_port_available(self, port):
        printy(f"Checking if port {port} is available")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            a = s.connect_ex(('localhost', port)) != 0
            printy(a)
            return a

    def start_server(self):
        while True:
            if self.exited_flag:
                self.endserver()
                break

            port = random.randint(50000, 65533)
            if self.is_port_available(port) and self.is_port_available(port+1):
                try:
                    ip_address = self.get_ip_address()
                    if ip_address is None:
                        printy("Failed to obtain IP address. Server cannot start.")
                        return

                    self.myClientPort = f"{ip_address}:{port}"
                    zmq_socket = self.context.socket(zmq.REP)
                    zmq_socket.bind(f"tcp://{self.myClientPort}")
                    break  # Exit the loop if binding is successful

                except zmq.ZMQError as e:
                    printy(f"Failed to bind to port {port}: {e}")
                    # Optionally, you could add a short delay here before retrying
                    time.sleep(1)
            else:
                printy(f"Port {port} is not available. Trying another port.")

        self.register(clientPort=f"{ip_address}:{port}",
                      public_key=self.wallet.get_public_key())

        self.get_peers()
        printy("Starting heartbeat manager")
        self.heartbeat_manager = HeartbeatManager(
            myClientPort=self.myClientPort, peers=self.peers, server_url=server_url, accounts=self.accounts)
        heartbeat_thread = threading.Thread(
            target=self.heartbeat_manager.run, daemon=True)
        heartbeat_thread.start()
        printy("Heartbeat manager started")
        while not self.heartbeat_manager.one_time:
            time.sleep(0.5)
        printy("Creating new thread since heartbeat manager has run once")
        thread = threading.Thread(target=self.broadcast_new_node)
        thread.start()

        self.initialised = True
        printy("New thread started")

        while True:
            message = zmq_socket.recv_string()
            zmq_socket.send_string(
                f"Successfully received message {message}. Sent from {self.myClientPort}")
            self.message_received(message)

    def broadcast_message(self, message):
        printy("Broadcasting message")
        responses = []
        encrypted_message = self.get_encrypted_message(message)
        printy(f"Peers: {self.peers}")

        for (clientPort, data) in self.peers.copy().items():
            if (clientPort != self.myClientPort):
                responses.append(self.private_send_message(
                    clientPort, encrypted_message))
            else:
                responses.append(self.privateSendToSelf(encrypted_message))

        return responses

    def privateSendToSelf(self, message):
        printy("Sending private message to self")
        try:
            self.message_received(message)
            return f"Private..Successfully received message {message}. Sent from {self.myClientPort}"
        except Exception as e:
            return f"Failed to send message {message} to self: {e}"

    def send_direct_encrypted_message(self, message, clientPort):
        printy("Sending direct message")
        encrypted_message = self.get_encrypted_message(message)
        if (clientPort == self.myClientPort):
            return self.privateSendToSelf(encrypted_message)
        return self.private_send_message(clientPort, encrypted_message)

    def get_peers(self):
        printy("Fetching peers")
        try:
            response = requests.get(f'{server_url}/peers')
            response.raise_for_status()
            peers_list = response.json()
            printy(f"Received peers: {peers_list}")
            for peer in peers_list:
                self.peers[peer['address']] = {
                    'lastcontacted': time.time(),
                    'public_key': peer['public_key']
                }

        except requests.RequestException as e:
            logging.error(f"Failed to fetch peers: {e}")
            printy('Failed to fetch peers')

    # def listen(self):
    #     printy("Starting tcp server...")
    #     server_thread = threading.Thread(
    #         target=self.start_server, daemon=True)
    #     server_thread.start()
    #     printy("Server thread started")

    def send_current_block_proposer(self, clientPort):
        message = {
            "type": MESSAGE_TYPE["block_proposer_address"],
            "address": self.block_proposer
        }

        self.send_direct_encrypted_message(message, clientPort)

    # FUNCTION CALLED WHEN A MESSAGE IS RECIEVED FROM ANOTHER CLIENT

    def message_received(self, message):

        # RECEIVED A MESSAGE
        printy(f"Received message: {message}")

        try:
            # CONVERT FROM JSON TO DICTIONARY
            data = json.loads(message)

        # ERROR IN JSON DECODING
        except json.JSONDecodeError:
            printy("Failed to decode JSON")
            return

        # CHECK IF SIGNATURE IS VALID
        if not ChainUtil.decryptWithSoftwareKey(data):
            printy("Invalid message recieved.")
            return

        # GET CLIENT PORT
        clientPort = data["clientPort"]
        printy("CLIENT PORT OF USER IS: ", clientPort)

        # PRINT THE TYPE OF MESSAGE
        printy("MESSAGE RECIEVED OF TYPE", data["type"])

        # IF BLOCKCAIN RECIEVED
        if data["type"] == MESSAGE_TYPE["chain"]:
            # TRY TO REPLACE IF LONGER CHAIN
            ret = self.blockchain.replace_chain(data["chain"])

            # IF NOT THE LONGEST CHAIN; DONT REPLACE ANYTHING ELSE AS THIS NODE'S DATA IS CLEARLY OUTDATED
            if not ret:
                printy("RECEIVED CHAIN WAS INVALID")
                return

            printy("REPLACED CHAIN")

            self.accounts.from_json(json_data=data["accounts"])
            printy("REPLACED ACCOUNTS")

            printy("ACCOUNTS: ", self.accounts.to_json())

            self.transaction_pool = TransactionPool.from_json(
                data["transaction_pool"])

            printy("REPLACED TRANSACTION POOL", self.transaction_pool)

            self.block_proposer = data["block_proposer"]
            printy("UPDATED BLOCK PROPOSER: ", self.block_proposer)

            # SET THE CURRENT RECEIVED BLOCK TO RECEIVE VOTES
            self.received_block = Block.from_json(
                data["received_block"]) if data["received_block"] else None
            printy("REPLACED RECEIVED BLOCK: ", self.received_block)

            
            #SET THE CURRENT RECEIVED BLOCK TO RECEIVE VOTES
            if data["received_block"]:
                self.received_block = Block.from_json(data["received_block"])
            
            # SET INITIALISED TO TRUE AND ALLOW USER TO GO TO MAIN PAGE
            if not self.initialised:
                self.initialised = True

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

            if self.block_proposer and self.block_proposer != block.validator:
                printy("RECEIVED BLOCK DOESN'T HAVE CORRECT VALIDATOR!")
                return

            # CHECK VALIDITY OF BLOCK & ITS TRANSACTIONS
            if (self.blockchain.is_valid_block(
                    block, self.transaction_pool, self.accounts)):

                # SET RECIEVED FLAG TO ALLOW VOTING
                self.block_received = True
                self.voted = False
                self.received_block = block
                self.accounts.add_sent_block(block.validator, block)

            else:
                printy("RECEIVED BLOCK DEEMED INVALID.")

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
            self.heartbeat_manager.addToClients(clientPort, data["public_key"])
            self.accounts.addANewClient(
                address=data["public_key"], clientPort=clientPort, userType=data["user_type"])

            if (clientPort != self.myClientPort):
                self.send_chain(clientPort)

        elif data["type"] == MESSAGE_TYPE["vote"]:
            self.handle_votes(data)

    def handle_votes(self, data):
        # CHECK IF THE VOTE IS VALID [FROM AN ACTIVE VALIDATOR]
        if (not self.accounts.accounts[data["address"]].isActive or
                not self.accounts.accounts[data["address"]].isValidator):
            printy("INVALID VOTE")
            return

        # IF NOT CURRENT BLOCK
        if data["block_index"] != self.received_block.index:
            printy("OLD VOTE RECEIVED")
            return

        # INCREMENT NUMBER OF VOTES FOR THE BLOCK
        self.received_block.votes.add(data["address"])
        votes = data["votes"]

        # INCREMENT VOTES FOR THE TRANSACTIONS
        transactions_dict = {
            transaction.id: transaction for transaction in self.received_block.transactions
        }

        for key, value in votes:
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
            "clientPort": self.myClientPort,
            "user_type": self.user_type
        }
        self.broadcast_message(message)

    def send_chain(self, clientPort):
        chain_as_json = [block.to_json() for block in self.blockchain.chain]
        block_json = (self.received_block.to_json() if self.received_block else None)
        message = {
            "type": MESSAGE_TYPE["chain"],
            "chain": chain_as_json,
            "accounts": self.accounts.to_json(),
            "transaction_pool": self.transaction_pool.to_json(),
            "block_proposer": self.block_proposer,
            "received_block": block_json
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

    def endserver(self):
        self.heartbeat_manager.stop()
        self.heartbeat_manager = None
        self.block_proposer = None
        self.block_received = None
        self.received_block = None
        self.context.destroy()
        self.accounts = Accounts()
