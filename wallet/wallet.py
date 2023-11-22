from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Wallet:
    def __init__(self, private_key=None, name=None, email=None):
        self.name = name
        self.email = email
        if not private_key:
            self.__private_key = RSA.generate(2048)
        else:
            self.__private_key = private_key

        self.__public_key = self.__private_key.publickey()

    def __str__(self):
        return f"Wallet -\n\tpublicKey: {self.get_public_key()}\n\tbalance: {self.balance}"

    def sign(self, data):
        data_hash = SHA256.new(data.encode())
        signature = pkcs1_15.new(self.__private_key).sign(data_hash)
        return signature
    
    
    def sign_hashed_data(self, data_hash):
        signature = pkcs1_15.new(self.__private_key).sign(data_hash)
        return signature

    def get_public_key(self):
        return self.__public_key.export_key().decode()

    def get_private_key(self):
        return self.__private_key.export_key().decode()