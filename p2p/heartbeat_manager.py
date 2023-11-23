import requests
import json
import threading
import time
import zmq
import logging

receive_timeout = 2000
send_timeout = 1000
heartbeat_interval = 10
logging.basicConfig(level=logging.INFO)


def printg(*args):
    joined_string = ' '.join(str(arg) for arg in args)
    try:
        print(f"\033[92m{joined_string}\033[00m")
    except:
        print(joined_string)


class HeartbeatManager:
    def __init__(self, myClientPort, heartbeat_timeout=20, peers={}, server_url="https://ujjwalaggarwal.pythonanywhere.com/app", accounts=None):
        self.myClientPort = myClientPort
        self.context = zmq.Context()
        self.peers = peers  # map of clientPort to dictionary of lastcontacted and public key
        self.heartbeat_timeout = heartbeat_timeout
        self.one_time = False
        self.heartbeat_counter = 0
        self.server_url = server_url
        self.accounts = accounts

    def private_send_message(self, clientPort, message):
        reply = None
        zmq_socket = self.context.socket(zmq.REQ)
        zmq_socket.setsockopt(zmq.RCVTIMEO, receive_timeout)
        zmq_socket.setsockopt(zmq.SNDTIMEO, send_timeout)
        try:
            tcpaddr = f"tcp://{clientPort}"
            zmq_socket.connect(tcpaddr)
            zmq_socket.send_string(message)
            reply = zmq_socket.recv_string()
        except Exception as e:
            # if e.errno == zmq.ETIMEDOUT:
            #     printg("TIMED OUT\n")
            logging.error(f"Error communicating with {clientPort}: {e}")
        finally:
            zmq_socket.close()
        return reply

    def start_heartbeat_client(self):
        printg(f"Starting heartbeat client")
        while True:
            printg(f"Current peers: {len(self.peers)}")
            self.heartbeat_decision(isFirstTime=not (self.one_time))
            while (self.heartbeat_counter > 0):
                time.sleep(3)
            self.remove_inactive_peers()
            self.one_time = True
            time.sleep(heartbeat_interval)

    def update_last_contacted(self, clientPort):
        if clientPort in self.peers:
            self.peers[clientPort]['lastcontacted'] = max(
                self.peers[clientPort]['lastcontacted'], time.time())

    def removeApi(self, clientPorts):
        printg("Removing with public key and address")
        printg(clientPorts)

        url = f'{self.server_url}/remove/'

        # printg the URL and the data to be sent
        printg(f"URL: {url}")
        printg(f"Data being sent: {clientPorts}")

        try:
            response = requests.post(url, json=clientPorts)
            printg(f"Remove api. Response from server: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Remove failed: {e}")
            return None

    def make_apicall_and_remove(self, clientPorts):
        thread = threading.Thread(target=self.removeApi, args=(clientPorts,))
        thread.start()
        for clientPort in clientPorts:
            self.accounts.make_inactive(self.peers[clientPort]['public_key'])
            del self.peers[clientPort]

    def remove_inactive_peers(self):
        current_time = time.time()
        inactive_peers = [port for port, data in self.peers.copy().items()
                          if port != self.myClientPort and current_time - data.get('lastcontacted', 0) > self.heartbeat_timeout]
        if len(inactive_peers) > 0:
            self.make_apicall_and_remove(inactive_peers)

    def send_heartbeat_to_peer(self, clientPort):
        printg("Sending heartbeat")
        heartbeat_message = json.dumps({
            "type": "heartbeat",
            "clientPort": self.myClientPort
        })
        return self.send_heartbeat(clientPort=clientPort, message=heartbeat_message)

    def should_send_heartbeat(self, data, isFirstTime):
        if isFirstTime:
            return True
        return time.time() - data['lastcontacted'] > heartbeat_interval

    def update_heartbeat_counter(self):
        self.heartbeat_counter -= 1

    def heartbeat_decision(self, isFirstTime=False):
        self.heartbeat_counter = len(self.peers)
        toremove = []
        for clientPort, data in self.peers.copy().items():
            if clientPort == self.myClientPort:
                self.update_heartbeat_counter()
                continue

            if self.should_send_heartbeat(data, isFirstTime):
                result = self.send_heartbeat_to_peer(clientPort)
                if result is not None:
                    toremove.append(result)
            else:
                self.update_heartbeat_counter()

        if len(toremove) > 0:
            printg(f"To remove {toremove}")
            self.make_apicall_and_remove(clientPorts=toremove)

    @staticmethod
    def getHeartBeatPort(clientPort):
        ip, port_str = clientPort.rsplit(':', 1)
        port = int(port_str)
        new_port = port + 1
        return f"{ip}:{new_port}"

    def send_heartbeat(self, message, clientPort):

        reply = self.private_send_message(clientPort=self.getHeartBeatPort(clientPort),
                                          message=message)
        if reply is None:
            printg(f"Peer {clientPort} is inactive")
            self.update_heartbeat_counter()
            return clientPort
        else:
            printg(f"Peer {clientPort} is active")
            self.update_last_contacted(clientPort)
            self.update_heartbeat_counter()
        return None

    def start_heartbeat_server(self):
        printg(
            f"Starting heartbeat server on port {self.getHeartBeatPort(self.myClientPort)}")
        zmq_socket = self.context.socket(zmq.REP)
        zmq_socket.bind(f"tcp://{self.getHeartBeatPort(self.myClientPort)}")

        printg("Creating new thread for client heartbeat")
        thread = threading.Thread(target=self.start_heartbeat_client)
        thread.start()
        printg("New thread started")

        while True:
            message = zmq_socket.recv_string()
            printg(f"Received heartbeat: {message}")
            zmq_socket.send_string(json.dumps(
                {"type": "heartbeat", "status": "success"}))
            message = json.loads(message)
            self.update_last_contacted(message['clientPort'])

    def addToClients(self, clientPort, public_key):
        print(f"Adding to clients to heartbeat peers{clientPort}")
        if (clientPort not in self.peers):
            self.peers[clientPort] = {
                'public_key': public_key,
                'lastcontacted': time.time()
            }

    def run(self):
        self.start_heartbeat_server()

    def stop(self):
        printg("Stopping heartbeat manager")
        self.context.destroy()
        printg("Heartbeat manager stopped")
