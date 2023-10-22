from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import uuid
import hashlib
import time


class ChainUtil:
    import hashlib

    @staticmethod
    def generate_32_byte_seed_from_timestamp():
        current_time = str(int(time.time()))
        hashed = hashlib.sha256(current_time.encode()).digest()
        return hashed

    @staticmethod
    def gen_key_pair():
        # Assume secret is a bytes-like object
        signing_key = SigningKey(
            seed=ChainUtil.generate_32_byte_seed_from_timestamp())
        return signing_key, signing_key.verify_key.encode(encoder=HexEncoder).decode()

    @staticmethod
    def id():
        return uuid.uuid1()

    @staticmethod
    def hash(data):
        data_string = str(data).encode()
        return hashlib.sha256(data_string).hexdigest()

    @staticmethod
    def verify_signature(public_key_hex, signature, data_hash):
        verify_key = VerifyKey(public_key_hex, encoder=HexEncoder)
        try:
            verify_key.verify(data_hash.encode(), signature.encode())
            return True
        except:
            return False

# # Example usage
# if __name__ == '__main__':
#     secret = b"some_secret_key_that_is_32bytes"
#     signing_key = ChainUtil.gen_key_pair(secret)
#     public_key = signing_key.verify_key.encode(encoder=HexEncoder).decode()
#     message = b"Hello, World!"
#     signature = signing_key.sign(message).signature
#     print(ChainUtil.verify_signature(public_key, signature.decode(), ChainUtil.hash(message)))
