import logging

from Crypto import Random

from structure.encryption.RSA.rsa_facade import RSA_facade
from structure.server_socket import Server_socket
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as cipher

class Server_socket_RSA(Server_socket):
    field_need_send_public_key = b'#@!$PppUbliCAnswer'


    def __init__(self, host, port, max_connections_count):
        super(Server_socket_RSA, self).__init__(host, port,
                                                max_connections_count)
        self.public, self.private=RSA_facade.get_private_and_public()
        self.sockets_piblic_keys = dict()

    def receiver(self, connection):
        data = connection.recv(1024)
        data,first_handshake = self.handshake(connection, data)

        if first_handshake or RSA_facade.isPublickKey(data):
            return data

        data = RSA_facade.decrypt(data, self.private)
        return data

    def send(self,connection,bytess):
        client = f"{connection.getpeername()[0]}:{connection.getpeername()[1]}"
        public_key_client= self.sockets_piblic_keys.get(client)

        if RSA_facade.isPublickKey(bytess):
            connection.send(bytess)
            return

        encrypt = RSA_facade.encrypt(bytess, public_key_client)
        connection.send(encrypt)

    def handshake(self, connection, data):
        if data.__eq__(Server_socket_RSA.field_need_send_public_key):
            return self.public,False

        client = f"{connection.getpeername()[0]}:{connection.getpeername()[1]}"

        if self.sockets_piblic_keys.__contains__(client):
            return data,False

        self.sockets_piblic_keys[client] = data
        return data,True

    def send_reply_bytes(self, conn, byttes):
        logging.debug("server reply to client")
        conn.send(byttes)
