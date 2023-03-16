from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# data = "I met aliens in UFO. Here is the map.".encode("utf-8")
def encrypt_file():
    data = open("tests/to_encrypt/file", "rb").read()
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    file_out = open("tests/encrypted_files/file.bin", "wb+")

    with open("key.pem", "wb+") as pkf:
        pkf.write(RSA.generate(2048).export_key())


    # recipient_key = RSA.import_key(open("receiver.pem").read())
    recipient_key = RSA.generate(2048)

    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(data)
    [file_out.write(x) for x in (enc_session_key, ciphertext)]
    file_out.close()
