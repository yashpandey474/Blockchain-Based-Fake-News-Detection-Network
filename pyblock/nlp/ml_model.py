import random

with open("moedl_1.pkl", "rb") as file:
    model = file["MODEL"]
    scaler = file["SCALER"]
def get_score(ipfs_address):
    # Generate a random double value between 0 and 1
    return random.random(0,1)
