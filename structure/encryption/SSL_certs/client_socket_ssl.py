import socket
import ssl

from structure.client_socket import Client_socket


class Client_socket_SSL(Client_socket):
    def __init__(self, hostTarget, portTarget):
        super(Client_socket_SSL, self).__init__(hostTarget,portTarget)

        asd=0

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock=ssl.wrap_socket(self.sock,cert_reqs=ssl.CERT_REQUIRED,ca_certs="cert.crt")
        self.sock=ssl_sock



if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    clientIMPL=Client_socket_SSL(ip, 7777)