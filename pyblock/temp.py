self.private_key = RSA.generate(2048)
self.public_key = self.private_key.publickey().export_key()
