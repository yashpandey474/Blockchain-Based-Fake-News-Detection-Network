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
# from blockchain.block import *
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
    def sign(private_key, data):
        data_str = json.dumps(data, cls = CustomJSONEncoder)
        private_key_RSA = RSA.import_key(private_key)
        data_hash = SHA256.new(data_str.encode())
        signature = pkcs1_15.new(private_key_RSA).sign(data_hash)
        return signature
    
    @staticmethod
    def sign_hashed_data(private_key, data_hash):
        private_key_1 = RSA.import_key(private_key)
        signature = pkcs1_15.new(private_key_1).sign(data_hash)
        return signature
    
    @staticmethod
    def verify_signature(public_key, signature, data):
        public_key_RSA = RSA.import_key(public_key)
        data_str = json.dumps(data, cls = CustomJSONEncoder)
        data_hash = SHA256.new(data_str.encode())
        
        try:
            pkcs1_15.new(public_key_RSA).verify(data_hash, signature)
            return True  # Signature is valid
        
        except (ValueError, TypeError):
            return False  # Signature is invalid
        
    @staticmethod
    def verify_hashed_signature(public_key, signature, data):
        data_hash = SHA256.new(data.encode())
        public_key_RSA = RSA.import_key(public_key)
        
        try:
            pkcs1_15.new(public_key_RSA).verify(data_hash, signature)
            return True 
        
        except (ValueError, TypeError):
            return False
        
    @staticmethod
    def encryptWithSoftwareKey(data):
        signature = ChainUtil.sign(config.VM_PRIVATE_KEY, data)
        data["VM_signature"] = signature
        return data

    @staticmethod
    def decryptWithSoftwareKey(data):
        signature_hex = data["VM_signature"]
        signature = binascii.unhexlify(signature_hex)
        del data["VM_signature"]
        
        
        if ChainUtil.verify_signature(config.VM_PUBLIC_KEY, signature, data):
            return data
        return None
    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.hex()
        elif isinstance(o, np.float32):
            return float(o)
            
        return json.JSONEncoder.default(self, o)
