from Crypto.PublicKey import RSA


def verify(private_key):

    try:
        rsa_private_key = RSA.import_key(private_key)
    except:
        return 0, "Invalid Key Format", None

    rsa_public_key = rsa_private_key.publickey()

    public_key_pem = rsa_public_key.export_key()

    print("Public Key (PEM format):")
    print(public_key_pem.decode())
    return 1, "Success", rsa_private_key


def gen_sk():
    key = RSA.generate(2048)
    return key


def verify_certificate(certificate_id):
    return certificate_id[: 4] == "ABCD"


if __name__ == "__main__":
    print(gen_sk().export_key().decode())
