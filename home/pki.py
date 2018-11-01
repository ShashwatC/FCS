from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64


def get_pair():
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.PEM,
                                               serialization.PublicFormat.PKCS1)

    # get private key in PEM container format
    pem = key.private_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                            encryption_algorithm=serialization.NoEncryption())

    # decode to printable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')

    print(private_key_str + "" + public_key_str)
    return private_key_str, public_key_str


# https://8gwifi.org/rsafunctions.jsp
# RSA/NONE/OAEPWithSHA1AndMGF1Padding
# https://8gwifi.org/RSAFunctionality?keysize=2048 Keysize 2048

def decrypt(cipher_text, private_key_str):
    cipher_text = base64.b64decode(cipher_text)
    private_key = private_key_str.encode()
    private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
    plaintext = private_key.decrypt(cipher_text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                              algorithm=hashes.SHA1(), label=None))
    return plaintext
