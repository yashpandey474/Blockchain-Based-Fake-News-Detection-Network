from Crypto.PublicKey import RSA


def verify(private_key):
    try:
        rsa_private_key = RSA.import_key(private_key)
    except:
        return 0, "incorrect key"
    rsa_public_key = rsa_private_key.publickey()

    public_key_pem = rsa_public_key.export_key()

    print("Public Key (PEM format):")
    print(public_key_pem.decode())
    return 1, "success"


def gen_sk():
    key = RSA.generate(2048)
    sk = key.export_key()
    return (sk.decode())


# if __name__ == "__main__":
#     print(verify("""-----BEGIN RSA PRIVATE KEY-----
#     MIIEpAIBAAKCAQEA9ZsywXYFaOshdTxWyxRJcwyDReY5RehY6KKu6iXyODDqvp2Y
#     XTYtMYjDInrwpwFArNGzqz299DVHC+BtvmBM414rUSHfoB5KC2175VYpNTXkPRpx
#     2r9PAS7JCVPKUW5SKdvfgWn2oUszJc7V09yJnLmVA/rXti70KSyK+Ew0A83jfsoL
#     OHn/n2B4DD2QK78wfLSngzoxvxv+W4lx1OrHOhiaGr8MkX32lsJcjvTMpoL4lYIa
#     21w6DSqOLBZp1s4r7Sqw3BXkB4oSOSDZx43IoAS3bDBlrNR0yZCELXfSn2vKT+rf
#     FsNsNdR6KXGW/AZssSTpxxS2HDyzrWik2m34DQIDAQABAoIBAFr85v3C0lg/G4MK
#     GoFbf6ZukUdY9gjO/fkZI8G80xI8FQsO6T5G7tE2AEyKzRKhpSsg+PXMhs2s2ygs
#     OZvYo0NsRJHnAaiY8AdxxP9+Pv/meiqk3F8Ulpkykumwr/gg7bFyMkgIUIUKjeVI
#     zfCR+C0ml20FBdsJZAzI4qb/3Bk3+GetCh8ba+u81avJHxXrglof9PqIvwodh2m/
#     2/S01uQ/0ESLMc4269/X1Q+vqiR7NFJtP3PPaR7+eURmIvb+ZdCWfogX/gShmxqO
#     9PLkS2g7q7EpV+u0eaViw0Ry+c1XuDipxZxx6TuOvbGiYqucwSvWVKson8K68GA6
#     Scw/XEUCgYEA9fAvO09b+OwFexEwlNy4MFLnyKM4Fyk/tisbHyLwTAYIAUzmXhiD
#     7F3QKG6Q0RQoibM5Liw7ha/6la5qg/D27Ku6KoYQb6YJbZNX4q+UM4YWyNmtR6En
#     YQe+3sybQoqO0/mN86+YtqF0rINL8xOYLMGEJNRxzs2Aesmtb0ZNcwMCgYEA/6eJ
#     bVUVQ4Rqa6Jl7thbnTX5tqpMrRjVS9WiBhjT4jJ3GeGPGebpjEv96Jf+vXnbDVLG
#     FY1owMfbDmyId09cvMBlz4mWQWTDvO3M71sbSeqV69JzgC3QTSEEaK8w6bPyZypn
#     m71297JXP9kdyB3KMk6NGWlOmAXWKNmqS9pGc68CgYBjc/tFmrPwl1EoES16JT9+
#     mygL5KUcCJwxCIFxN+nAdHfsPrKxvmwqu00f7IY3ZlV2SbmHyG9RgnZs7Rk5vcm8
#     rz0bURd4bsZFP1481w+xPjocgpol6y9Hd6Bh7I+keu+DHNmgf5Pb1rKdyIKAC55w
#     CtlrI1XacRPRk5jE9MMBDQKBgQDaHaxIVXEA27aYAkQJVRpEtMpKKF2mySshujC0
#     FvafZALtV93pcXMMucD1cshqC87yPQ63UKBw6ZJhagO8Fz+94kB6op5JSJkfVZul
#     EwvjMnuaaUEVuQCg7Wx/jAilO1uy3SDsZOddSRDbbnfURmY+KXqEla3yUfh3fc2n
#     TaESDQKBgQDzQSRuNxxGNUcUHZX7y45p6gUp00jkraY+w4W2X/9XzvLUnbX95oEj
#     sw3WA8wFE1tfK7isNcs9ew3Xik1Ur+xEtnpePraDz8aQIwQgr0LZMbfauG1j7SlZ
#     Qph2gx5UoZY6GVFRMonsro14XBI4imnKLhWekf1faGiwEhGl2IXeIg==
#     -----END RSA PRIVATE KEY-----"""))