from Crypto.PublicKey import RSA

private_key = RSA.generate(2048)
public_key = private_key.publickey().export_key()

print(private_key.decode())