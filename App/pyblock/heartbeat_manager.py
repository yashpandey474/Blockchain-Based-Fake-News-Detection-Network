import json
import threading
import time
import zmq
import logging
receive_timeout = 1000
send_timeout = 1000
heartbeat_interval = 5
logging.basicConfig(level=logging.INFO)


class HeartbeatManager:
    def __init__(self, myClientPort, context, heartbeat_timeout=20, peers={}):
        self.myClientPort = myClientPort
        self.context = context
        self.peers = peers  # map of clientPort to dictionary of lastcontacted and public key
        self.heartbeat_timeout = heartbeat_timeout
        self.one_time = False
        self.heartbeat_counter = 0

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
            #     print("TIMED OUT\n")
            logging.error(f"Error communicating with {clientPort}: {e}")
        finally:
            zmq_socket.close()
        return reply

    def start_heartbeat_client(self):
        print(f"Starting heartbeat client")
        while True:
            print(f"Current peers: {len(self.peers)}")
            self.heartbeat_decision(isFirstTime=~self.one_time)
            while (self.heartbeat_counter > 0):
                time.sleep(3)
            self.remove_inactive_peers()
            self.one_time = True
            time.sleep(heartbeat_interval)

    def update_last_contacted(self, clientPort):
        if clientPort in self.peers:
            self.peers[clientPort]['lastcontacted'] = max(
                self.peers[clientPort]['lastcontacted'], time.time())

    def remove_inactive_peers(self):
        current_time = time.time()
        inactive_peers = [port for port, data in self.peers.copy().items()
                          if port != self.myClientPort and current_time - data.get('lastcontacted', 0) > self.heartbeat_timeout]
        for port in inactive_peers:
            del self.peers[port]

    def send_heartbeat_to_peer(self, clientPort):
        print("Sending heartbeat")
        heartbeat_message = json.dumps({
            "type": "heartbeat",
            "clientPort": self.myClientPort
        })
        self.send_heartbeat(clientPort=clientPort, message=heartbeat_message)

    def should_send_heartbeat(self, data, isFirstTime):
        if isFirstTime:
            return True
        return time.time() - data['lastcontacted'] > heartbeat_interval

    def update_heartbeat_counter(self):
        self.heartbeat_counter -= 1

    def heartbeat_decision(self, isFirstTime=False):
        self.heartbeat_counter = len(self.peers)

        for clientPort, data in self.peers.copy().items():
            if clientPort == self.myClientPort:
                self.update_heartbeat_counter()
                continue

            if self.should_send_heartbeat(data, isFirstTime):
                self.send_heartbeat_to_peer(clientPort)
            else:
                self.update_heartbeat_counter()

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
            print(f"Peer {clientPort} is inactive")
            del self.peers[clientPort]
        else:
            print(f"Peer {clientPort} is active")
            self.update_last_contacted(clientPort)
        self.heartbeat_counter -= 1

    def start_heartbeat_server(self):
        print(
            f"Starting heartbeat server on port {self.getHeartBeatPort(self.myClientPort)}")
        zmq_socket = self.context.socket(zmq.REP)
        zmq_socket.bind(f"tcp://{self.getHeartBeatPort(self.myClientPort)}")

        print("Creating new thread for client heartbeat")
        thread = threading.Thread(target=self.start_heartbeat_client)
        thread.start()
        print("New thread started")

        while True:
            message = zmq_socket.recv_string()
            print(f"Received heartbeat: {message}")
            zmq_socket.send_string(json.dumps(
                {"type": "heartbeat", "status": "success"}))
            message = json.loads(message)
            self.update_last_contacted(message['clientPort'])

    def addToClients(self, clientPort, publicKey):
        if (clientPort not in self.peers):
            self.peers[clientPort] = {
                'publicKey': publicKey,
                'lastcontacted': time.time()
            }

    def run(self):
        self.start_heartbeat_server()
