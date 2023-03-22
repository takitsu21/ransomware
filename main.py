#!/usr/bin/env python

import os
import time
from src import encrypt
from src import decrypt
from src import logger


def clean(rootdir):
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            fpath: str = os.path.abspath(os.path.join(subdir, file))
            if fpath.endswith(".bin") and os.path.exists(fpath):
                os.remove(fpath)


def main(rootdir):
    clean(rootdir)
    start = time.time()
    rsa_aes = encrypt.RSAAESEncryption()
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            fpath = os.path.abspath(os.path.join(subdir, file))
            rsa_aes.encrypt(fpath)
    end = time.time()
    logger.debug(f"Time elapsed: {end - start}s")


if __name__ == '__main__':
    main("tests/to_encrypt/")
