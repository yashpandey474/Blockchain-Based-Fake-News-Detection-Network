from nacl.secret import SecretBox
from nacl.utils import random
from nacl.encoding import HexEncoder, RawEncoder
from nacl.signing import SigningKey, VerifyKey
import hashlib
import time
import uuid
import numpy as np
import json
import pyblock.config as config
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

class ChainUtil:


    @staticmethod
    def generate_32_byte_seed_from_timestamp():
        current_time = str(int(time.time()))
        hashed = hashlib.sha256(current_time.encode()).digest()
        return hashed

    @staticmethod
    def gen_key_pair():
        signing_key = SigningKey(
            ChainUtil.generate_32_byte_seed_from_timestamp())
        return signing_key, signing_key.verify_key.encode(encoder=HexEncoder).decode()

    @staticmethod
    def id():
        return uuid.uuid1()

    @staticmethod
    def hash(data):
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    @staticmethod
    def sign(data):
        # Serialize the dictionary to a JSON string
        data_str = json.dumps(data, cls = CustomJSONEncoder)
        private_key = RSA.import_key(config.VM_PRIVATE_KEY)
        data_hash = SHA256.new(data_str.encode())
        signature = pkcs1_15.new(private_key).sign(data_hash)
        return signature

    @staticmethod
    def verify_signature(signature, data):
        public_key = RSA.import_key(config.VM_PUBLIC_KEY)
        data_str = json.dumps(data, cls = CustomJSONEncoder)
        data_hash = SHA256.new(data_str.encode())
        try:
            pkcs1_15.new(public_key).verify(data_hash, signature)
            return True  # Signature is valid
        except (ValueError, TypeError):
            return False  # Signature is invalid
    @staticmethod
    def verify_hashed_signature(public_key, signature, data_hash):
        public_key_1 = RSA.import_key(public_key)
        
        try:
            pkcs1_15.new(public_key_1).verify(data_hash, signature)
            return True 
        
        except (ValueError, TypeError):
            return False
        
    # @staticmethod
    def encryptWithSoftwareKey(data):
        signature = ChainUtil.sign(data)
        signature_hex = binascii.hexlify(signature).decode('utf-8')
        print("SIGNATURE = ", signature, "DATA = ", data)
        data["VM_signature"] = signature
        return data

    # @staticmethod
    def decryptWithSoftwareKey(data):
        signature_hex = data["VM_signature"]
        signature = binascii.unhexlify(signature_hex)
        del data["VM_signature"]
        
        print("SIGNATURE  = ", signature, "DATA = ", data)
        if ChainUtil.verify_signature(signature, data):
            return data
        
        return None
    
    # @staticmethod
    # def encryptWithSoftwareKey(data):
    #     public_key = RSA.import_key(config.VM_PUBLIC_KEY)
    #     cipher = PKCS1_OAEP.new(public_key)
    #     encrypted_data = cipher.encrypt(data.encode())
    #     return encrypted_data

    # @staticmethod
    # def decryptWithSoftwareKey(encrypted_data):
        
    #     private_key = RSA.import_key(config.VM_PRIVATE_KEY)
    #     cipher = PKCS1_OAEP.new(private_key)
    #     decrypted_data = cipher.decrypt(encrypted_data)
    #     return decrypted_data



# Example usage, the secret must be provided in config module as VM_PRIVATE_KEY
# if __name__ == '__main__':
#     # ... the rest of your example usage
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.hex()
        elif isinstance(o, np.float32):
            return float(o)
        return json.JSONEncoder.default(self, o)
