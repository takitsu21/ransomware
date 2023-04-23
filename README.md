# ransomware

This is a simple ransomware written in Python. It uses AES-128 encryption to encrypt files on the system and RSA-2048 to encrypt the AES key. The AES key is then encrypted with the public key of the attacker. The attacker can then decrypt the AES key with their private key and decrypt the files.

# TODO

- [ ] Add TLS/SSL certificates
- [X] Add API authentication
- [ ] Add API endpoints for example:
    - [ ] GET /hardware/{uuid}
    - [ ] POST /hardware/{uuid}
    - [ ] GET /files/{uuid}
    - [ ] POST /files/{uuid}
    - [X] GET /keys/public_key/{uuid}
    - [X] GET /keys/private_key/{uuid}
    - [X] GET /keys/aes_key/{uuid}
