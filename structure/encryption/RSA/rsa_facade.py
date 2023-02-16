import bz2
import pickle

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as cipher
from Crypto import Random

from structure.server_socket import Server_socket


class RSA_facade:
    @staticmethod
    def encrypt(bytess, pubKey):
        if len(bytess)==0:
            return bytess

        key = rsa.importKey(pubKey)
        cip = cipher.new(key)

        if len(bytess)>100:
            obj= Rsa_Limit_chunks(bytess,cip)
            serialized= Server_socket.serialize_object(obj)
            return serialized

        try:
            result=cip.encrypt(bytess)
            return result
        except ValueError as ept:
            sad=0


        return None

    @staticmethod
    def decrypt(bytess, private):
        if len(bytess) == 0:
            return bytess

        key = rsa.importKey(private)
        cip = cipher.new(key)


        try:
            obj = pickle.loads(bytess)
            if type(obj).__name__ is "Rsa_Limit_chunks":
                return obj.encrypt_chunks(cip)
        except Exception as norm:
        # except pickle.UnpicklingError as norm:
            ads=0

        try:
            result=cip.decrypt(bytess, None)
        except Exception as norm:
            ads = 0

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

class Rsa_Limit_chunks:
    def __init__(self,bytes_input,cipher_by_key):
        n = 100
        chunks = [bytes_input[i:i + n] for i in range(0, len(bytes_input), n)]

        self.chunks_encrypt=[cipher_by_key.encrypt(i) for i in chunks]
    def encrypt_chunks(self,cipher_by_key):
        encrypted=[cipher_by_key.decrypt(i, None) for i in self.chunks_encrypt]
        return b''.join(encrypted)






if __name__ == '__main__':
    pub,priv= RSA_facade.get_private_and_public()

    bbbb=b"adaadsfadsfhfadafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhdsfhghhdghhfaadsfhfadafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhdsfhghhdghdafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhdsfhghhdghdsfhfadafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhdsfhghhdghsfhfadafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhadsfhfadafhdfsagsdfhsgsdfhghsddfsghsdgsdghdffhdsfhghhdghdsfhghhdgh"
    count= len(bbbb)
    print(count)
    RSA_facade.encrypt(bbbb,pub)