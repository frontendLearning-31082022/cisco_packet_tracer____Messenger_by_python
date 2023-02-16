from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as cipher
from Crypto import Random

class RSA_facade:
    @staticmethod
    def encrypt(bytess, pubKey):
        if len(bytess)==0:
            return bytess

        key = rsa.importKey(pubKey)
        cip = cipher.new(key)
        return cip.encrypt(bytess)

    @staticmethod
    def decrypt(bytess, private):
        if len(bytess) == 0:
            return bytess

        key = rsa.importKey(private)
        cip = cipher.new(key)
        result=cip.decrypt(bytess, None)
        return result

    @staticmethod
    def get_private_and_public():
        from Crypto.PublicKey import RSA
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        public = key.publickey().exportKey()
        private = key.exportKey()
        return public, private

    @staticmethod
    def isPublickKey(bytess):
        try:
            if bytess.decode("utf-8").index("BEGIN PUBLIC KEY") > 0:
                return True
        except:
            asd=0

        return False

