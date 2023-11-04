from nacl.secret import SecretBox
from nacl.utils import random
from nacl.encoding import HexEncoder, RawEncoder
from nacl.signing import SigningKey, VerifyKey
import hashlib
import time
import uuid
import pyblock.config as config
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class ChainUtil:
    @staticmethod
    def verify_signature(public_key: str, signature: str, data_hash: str) -> bool:
        try:
            # data_hash = SHA256.new(data.encode())
            pkcs1_15.new(public_key).verify(data_hash, signature)
            return True
        
        except (ValueError, TypeError):
            return False 

    @staticmethod
    def generate_32_byte_seed_from_timestamp():
        current_time = str(int(time.time()))
        hashed = hashlib.sha256(current_time.encode()).digest()
        return hashed

    @staticmethod
    def gen_key_pair():
        signing_key = SigningKey(ChainUtil.generate_32_byte_seed_from_timestamp())
        return signing_key, signing_key.verify_key.encode(encoder=HexEncoder).decode()

    @staticmethod
    def id():
        return uuid.uuid1()

    @staticmethod
    def hash(data):
        return hashlib.sha256(str(data).encode()).hexdigest()

    @staticmethod
    def encryptWithSoftwareKey(data):
        if isinstance(data, str):
            data = data.encode()  # Ensure the data is in bytes
        key = config.VM_PRIVATE_KEY.encode()  # Ensure the key is in bytes
        box = SecretBox(key, encoder=HexEncoder)
        nonce = random(SecretBox.NONCE_SIZE)
        encrypted = box.encrypt(data, nonce, encoder=RawEncoder)
        return (nonce + encrypted).hex()

    @staticmethod
    def decryptWithSoftwareKey(data):
        if isinstance(data, str):
            data = bytes.fromhex(data)  # Decode if data is in hex string
        key = config.VM_PRIVATE_KEY.encode()  # Ensure the key is in bytes
        box = SecretBox(key, encoder=HexEncoder)
        nonce = data[:SecretBox.NONCE_SIZE]
        encrypted = data[SecretBox.NONCE_SIZE:]
        decrypted = box.decrypt(encrypted, nonce, encoder=RawEncoder)
        return decrypted.decode()  # Return as a string

# Example usage, the secret must be provided in config module as VM_PRIVATE_KEY
# if __name__ == '__main__':
#     # ... the rest of your example usage
