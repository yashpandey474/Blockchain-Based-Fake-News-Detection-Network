from flask import Flask, request
import json
import ast

app = Flask(__name__)
peer_path = "./peers.json"


@app.route('/app/clear/', methods=['POST'])
def magic():
    open(peer_path, "w")
    return []


@app.route('/app/register/', methods=['POST'])
def register():
    peer_data = request.json
    with open(peer_path, "a") as f:
        f.write(str(peer_data) + "\n")
    return list_peers()


@app.route('/app/peers', methods=['GET'])
def list_peers():
    with open(peer_path, "r") as file:
        lines = file.readlines()

    parsed_peers = []
    for line in lines:
        # Convert single quotes to double quotes and parse as a Python dictionary
        data_dict = ast.literal_eval(line.replace("'", '"'))
        parsed_peers.append(data_dict)

    return json.dumps(parsed_peers)


@app.route('/app/remove/', methods=['POST'])
def remove():
    peer_data = list(request.json)
    with open(peer_path, "r") as file:
        lines = file.readlines()

    with open(peer_path, "w") as file:
        for line in lines:
            if not (any(peer in line for peer in peer_data)):
                file.write(line)

    return list_peers()


if __name__ == '__main__':
    print("starting")
    app.run(port=10001)
