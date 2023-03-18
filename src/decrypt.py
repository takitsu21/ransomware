from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

AES_IV_SIZE = 16
# Decrypt the session key with the private RSA key


def decrypt_file():
    file_in = open("tests/encrypted_files/file.bin", "rb")

    private_key = RSA.import_key(open("key.pem").read())

    enc_session_key, iv, ciphertext = \
        [file_in.read(x)
         for x in (private_key.size_in_bytes(), AES_IV_SIZE, -1)]
    # enc_session_key = file_in.read(private_key.size_in_bytes())
    # iv = file_in.read(16)
    # ciphertext = file_in.read(-1)
    print("enc_session_key", enc_session_key)
    # print("ciphertext: ", ciphertext)
    # for x in (private_key.size_in_bytes(), -1):
    # for x in (private_key.size_in_bytes(), -1):
    #     print(file_in.read(x))
    file_in.close()
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv=iv)
    data = cipher_aes.decrypt(ciphertext)
    print("Decrypted data: ", data.rstrip())
    with open("tests/decrypted_files/file", "w+") as f:
        f.write(data.rstrip().decode("utf-8"))
