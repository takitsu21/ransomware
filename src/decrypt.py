from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


# Decrypt the session key with the private RSA key
def decrypt_file():
    file_in = open("tests/encrypted_files/file.bin", "rb")

    private_key = RSA.import_key(open("key.pem").read())

    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
    file_in.close()

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    data = cipher_aes.decrypt(ciphertext)
    with open("tests/decrypted_files/file", "w+") as f:
        f.write(data)
