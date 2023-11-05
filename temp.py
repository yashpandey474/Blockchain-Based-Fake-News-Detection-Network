from Crypto.PublicKey import RSA

private_key = RSA.generate(2048)
public_key = private_key.publickey()

print(private_key.export_key().decode())
print(public_key.export_key().decode())