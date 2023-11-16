import streamlit as st
import requests
import zmq
import logging
import threading
import socket
import queue
# Improved logging
logging.basicConfig(level=logging.INFO)

# Configuration
server_url = 'http://65.1.130.255/app'  # Local server URL
default_port = 6969
default_public_key = '123'
myaddress = 0
# Global variables
peers = []
context = zmq.Context()
# Initialize session state
if 'received_messages' not in st.session_state:
    st.session_state['received_messages'] = []

port = st.number_input("Enter the server port",
                       min_value=1024, max_value=65535, value=default_port)


def register(public_key, address):
    print("Registering with public key and address")
    data = {'public_key': public_key, 'address': address}
    try:
        response = requests.post(f'{server_url}/register', json=data)
        print(f"Response from server: {response}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Registration failed: {e}")
        return None


def get_private_network_ip_address():
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


def get_ip_address():
    print("Getting public IP address")
    try:
        response = requests.get("https://httpbin.org/ip")
        ip_address = response.json().get('origin')
        print(f"Obtained public IP address: {ip_address}")
        return ip_address
    except Exception as e:
        logging.error(f"Error obtaining public IP address: {e}")
        return None


def start_server(port):
    print(f"Starting server on port {port}")
    if port < 1024 or port > 65535:
        st.error(
            "Invalid port number. Please enter a port number between 1024 and 65535.")
        return
    ip_address = get_ip_address()
    if ip_address is None:
        st.error("Failed to obtain IP address. Server cannot start.")
        return

    zmq_socket = context.socket(zmq.REP)
    zmq_socket.bind(f"tcp://0.0.0.0:{port}")
    myaddress = f"{ip_address}:{port}"
    register(address=f"{ip_address}:{port}", public_key=default_public_key)

    while True:
        message = zmq_socket.recv_string()
        print(f"Received message: {message}")
        zmq_socket.send_string(
            f"Received message {message}. Sent from {myaddress}")


def broadcast_message(message, context):
    print("Broadcasting message")
    responses = []
    newpeers = get_peers()
    print(f"Peers: {newpeers}")
    for peer in newpeers:
        zmq_socket = context.socket(zmq.REQ)
        # Receive timeout in milliseconds
        zmq_socket.setsockopt(zmq.RCVTIMEO, 5000)
        # Send timeout in milliseconds
        zmq_socket.setsockopt(zmq.SNDTIMEO, 5000)
        try:
            tcpaddr = f"tcp://{peer['address']}"
            print(f"Sending message to {tcpaddr}")
            zmq_socket.connect(tcpaddr)
            zmq_socket.send_string(message)
            reply = zmq_socket.recv_string()
            responses.append(reply)
            print(f"Received reply from {peer['address']}: {reply}")
        except Exception as e:
            logging.error(f"Error communicating with {peer}: {e}")
        finally:
            zmq_socket.close()
    return responses


def get_peers():
    print("Fetching peers")
    try:
        response = requests.get(f'{server_url}/peers')
        response.raise_for_status()
        peers_list = response.json()
        print(f"Received peers: {peers_list}")
        return peers_list
    except requests.RequestException as e:
        logging.error(f"Failed to fetch peers: {e}")
        st.error('Failed to fetch peers')
        return []


# Streamlit UI
st.title('Peer-to-Peer Communication App')

if st.button('Sign Up and Start Server'):
    server_thread = threading.Thread(
        target=start_server, args=(port,), daemon=True)
    server_thread.start()
    print("Server thread started")

if st.button('Refresh Peers'):
    peers = get_peers()
    print(f"Refreshed peers: {peers}")

st.header('Peers')
if peers:
    st.json(peers)
else:
    st.write('No peers available')

st.header('Send a Message')
message = st.text_area('Message')
if st.button('Send Message'):
    responses = broadcast_message(message, context)
    print(f"Message sent, responses: {responses}")
    if responses:
        st.success('Message sent successfully')
        st.write('Responses:', responses)
    else:
        st.error('Failed to send message')
