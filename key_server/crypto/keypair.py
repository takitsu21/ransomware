import logging
from Crypto.PublicKey import RSA


logger = logging.getLogger("key_server")

RSA_DEFAULT_KEY_SIZE = 2048


class KeyPair:
    """
    RSA/AES encryption class

    This class is used to encrypt files using RSA and AES.

    The RSA key pair is generated on initialization and the private key is stored in a file.
    The public key is used to encrypt the AES session key
    and the AES session key is used to encrypt the file data.

    The encrypted data is written to a file with the same name as the original
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize the encryption class

        :param private_key: The private key to use for encryption
        :param kwargs: Additional keyword arguments
        """
        self.rsa_key_size = kwargs.get("rsa_key_size", RSA_DEFAULT_KEY_SIZE)
        self._public_key = None
        self._private_key = None
        self.keypair = self._generate_rsa_key()

    def __repr__(self) -> str:
        return f"RSAAESEncryption(rsa_key_size={self.rsa_key_size})"

    @property
    def private_key(self):
        """
        Export the private key
        """
        return self._private_key

    @property
    def public_key(self):
        """
        Export the public key
        """
        return self._public_key

    def _generate_rsa_key(self):
        """
        Generate a new RSA key pair

        :return: The generated RSA key pair
        """
        logger.info(f"Generating RSA key pair with size: {self.rsa_key_size}")
        keypair = RSA.generate(self.rsa_key_size)
        try:
            self._public_key = keypair.publickey().export_key()
            self._private_key = keypair.export_key()
        except Exception as e:
            logger.error(f"Error while exporting key pair: {e}")
        return keypair
