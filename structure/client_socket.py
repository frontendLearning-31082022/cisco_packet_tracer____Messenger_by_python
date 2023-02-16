import random
import socket
import logging
import time


class Client_socket:

    @staticmethod
    def tries_send():
        return 5

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, hostTarget, portTarget):
        self.clientPort = None
        self.create_socket()

        self.__hostTarget = hostTarget
        self.__portTarget = portTarget
        self.clientPort=None

    def create_socket(self):
        self.sock = socket.socket()
        if self.clientPort is None:
            # port storage need on server
            port_num=random.randint(30000, 40000)

            self.sock.bind(('0.0.0.0',port_num))
            self.clientPort=port_num
        else:
            self.sock.bind(('0.0.0.0',self.clientPort))

    def connect(self,hostTarget,portTarget):
        time.sleep(1)
        # try:
        self.sock.connect((hostTarget, portTarget))
        # except OSError:
        #     time.sleep(1000)
        #     self.sock.connect((hostTarget, portTarget))


    def send_echo(self, msg):
        self.create_socket()
        logging.debug("send() socket init")
        self.connect(self.__hostTarget, self.__portTarget)
        logging.debug("send() clien socket connected")

        tries=Client_socket.tries_send()
        while  tries> 0:
            self.send(msg.encode())
            logging.debug("send() client")
            data = self.recieve_by_socket()
            if data.__eq__(msg.encode):
                break

        self.sock.close()
        logging.debug("send() client socket close")



    def send_echo_object(self, bytess):
        success_operation=False

        self.create_socket()
        logging.debug("send() socket init")
        self.connect(self.__hostTarget, self.__portTarget)
        logging.debug("send() clien socket connected")

        tries=Client_socket.tries_send()
        while tries > 0:
            self.send_by_socket(bytess)
            logging.debug("send() client")
            data = self.recieve_by_socket()
            if data.__eq__(bytess):
                success_operation=True
                break

        self.sock.close()
        logging.debug("send() client socket close")

        return success_operation

    def send_answer_get(self, msg):
        self.create_socket()
        logging.debug("send() socket init")
        self.connect(self.__hostTarget, self.__portTarget)
        logging.debug("send() clien socket connected")

        answer=None
        tries = Client_socket.tries_send()
        while tries > 0:
            self.send_by_socket(msg.encode())
            logging.debug("send() client")
            answer = self.recieve_by_socket()
            if not answer is None:
                tries = tries - 1
                break

        self.sock.close()
        logging.debug("send() client socket close")
        return answer

    def send_by_socket(self, bytess):
        self.sock.send(bytess)

    def recieve_by_socket(self):
        logging.debug("send() client wait receive")
        data = self.sock.recv(1024)
        return data
