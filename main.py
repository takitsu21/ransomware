#!/usr/bin/env python

import src.logger as logger
import src.encrypt as encrypt
import src.decrypt as decrypt


if __name__ == '__main__':
    encrypt.encrypt_file()
    decrypt.decrypt_file()
