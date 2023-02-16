import hashlib
import logging
import socket
from base64 import b64decode

from Crypto import Random, Cipher

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as cipher

from structure.client_socket import Client_socket
from structure.encryption.RSA.rsa_facade import RSA_facade
from structure.encryption.RSA.server_socket_RSA import Server_socket_RSA


class Client_socket_RSA(Client_socket):

    def __init__(self, hostTarget, portTarget):
        super(Client_socket_RSA, self).__init__(hostTarget, portTarget)
        self.__hostTarget = hostTarget
        self.__portTarget = portTarget

        self.public, self.private = RSA_facade.get_private_and_public()

        self.handshake_ok = False
        self.handshake()

    # need double check keys
    def handshake(self):
        if self.handshake_ok:
            return
        self.create_socket()
        self.connect(self.__hostTarget, self.__portTarget)
        tries = Client_socket.tries_send()
        while tries > 0:
            self.sock.send(self.public)
            logging.debug("send() public")
            data = self.sock.recv(2048)
            if data.__eq__(self.public):
                break
            else:
                raise Exception("Can't send public")

        self.sock.close()
        logging.debug("send() public sended")

        self.create_socket()
        self.connect(self.__hostTarget, self.__portTarget)
        tries = Client_socket.tries_send()
        while tries > 0:
            self.sock.send(Server_socket_RSA.field_need_send_public_key)
            logging.debug("send() to get server public key")
            data = self.sock.recv(2048)
            if RSA_facade.isPublickKey(data):
                self.server_public_key = data
                self.handshake_ok = True
                break
            else:
                raise Exception("Can't send public")

        self.sock.close()
        logging.debug("send() public sended")

    def send_by_socket(self, bytess):
        encrypt=RSA_facade.encrypt(bytess,self.server_public_key)
        self.sock.send(encrypt)

    def recieve_by_socket(self):
        logging.debug("send() client receive rsa")
        data = self.sock.recv(2048)
        data=RSA_facade.decrypt(data,self.private)
        return data

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    chat_client = Client_socket_RSA(ip, 7777)
