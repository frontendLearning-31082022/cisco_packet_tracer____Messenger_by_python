import abc
import multiprocessing
import pickle
import queue
import socket
import threading
from threading import Thread

import logging

import select

logging.basicConfig(level=logging.DEBUG)


class Server_socket(Thread):
    field_get_info="@getINFOserver"
    field_username = "username=\"{}\""

    def __init__(self, host, port, max_connections_count):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.max_connections_count = max_connections_count

    def run(self):
        self.queue_reqs = multiprocessing.Queue()
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections_count)

        # self.socket.settimeout(3)
        self.start_listen()

    @staticmethod
    def serialize_object(object):
        return pickle.dumps(object)

    def start_listen(self):
        while True:
            logging.debug("server listen new clients")
            try:
                conn, addr = self.socket.accept()
            except(TimeoutError):
                continue

            client_handler = threading.Thread(target=self.handle_one_client,
                                              args=(conn,))
            client_handler.start()

    def handle_one_client(self, conn):
        logging.debug("server client connected")

        data = self.read_data(conn)

        if self.check_data_need_storage(data):
            self.queue_reqs.put(data)

        conn.close()
        logging.debug("server connection close")

    def send_answer_bytes(self, conn, data_all):
        pass

    def read_data(self, conn):
        logging.debug("server receive data")
        self.socket.settimeout(3)
        data_all = b""
        while True:
            read, write, err = select.select([conn], [], [])
            if conn in read:
                data=self.receiver(conn)
            data_all = data_all + data

            answer_sended = self.send_answer_bytes(conn, data_all)
            if not answer_sended:
                self.send_reply_bytes(conn, data_all)
            if not data:
                break


            
        return data_all

    def send_reply_bytes(self, conn, byttes):
        logging.debug("server reply to client")
        self.send(conn,byttes)

    @abc.abstractmethod
    def check_data_need_storage(self, data):
        return False

    def send(self,connection,bytess):
        connection.send(bytess)

    def receiver(self,connection):
        data = connection.recv(1024)
        return data






