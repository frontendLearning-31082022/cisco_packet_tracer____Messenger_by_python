import hashlib

import Crypto.PublicKey.RSA
from Crypto.PublicKey import RSA

# https://devtut.github.io/python/sockets-and-message-encryption-decryption-between-client-and-server.html#client-side-implementation
class RSA_struct:
    @staticmethod
    def step1_client_rsa():
        key_generator= RSA.generate(2048)
        public = key_generator.publickey().exportKey()
        return key_generator,public

    @staticmethod
    def step2_hash_sha1_public_key(public):
        return hashlib.sha1(public)

    @staticmethod
    def main():
        key_generator, public = RSA_struct.step1_client_rsa()
        hash = RSA_struct.step2_hash_sha1_public_key(public)
        hex_digest = hash.hexdigest()
        asd = 0



# if __name__ == '__main__':
