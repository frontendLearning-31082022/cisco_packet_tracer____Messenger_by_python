import _pickle
import pickle
import re
import socket
import time
import types
from collections import deque
from datetime import datetime
from logging.handlers import QueueListener
from tkinter import END

from structure.encryption.RSA.server_socket_RSA import Server_socket_RSA
from structure.gui_chat import Gui_chat
from structure.server_socket import Server_socket


class MessagePattern:
    def __init__(self, from_user, to_user, message):
        self.from_user = from_user
        self.to_user = to_user
        self.message = message
        self.date = datetime.now()

    def __str__(self):
        return f"{self.date} Message from {self.from_user} to {self.to_user}: {self.message}"





class Chat_server():
    field_change_user = "выберите пользователя"

    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())

        # self.module_server_socket = Server_socket(self.ip, 7777, 10)
        self.module_server_socket = Server_socket_RSA(self.ip, 7777, 10)

        self.module_server_socket.send_answer_bytes = types.MethodType(
            self.send_answer_bytes_chat, self.module_server_socket)

        self.override_socket_need_data_collect()

        self.module_server_socket.start()

        self.users_chats = {}
        time.sleep(2)

        # need subsribe on event
        while True:
            if not self.module_server_socket.queue_reqs.empty():
                data = self.module_server_socket.queue_reqs.get()
                self.socket_income(data)

    def socket_income(self, data):
        try:
            data_recog = pickle.loads(data)
            self.new_message(data_recog)
        except(_pickle.UnpicklingError):
            pass

    def send_info_data_to_client(self, string_comand):
        recog = string_comand.replace(Server_socket.field_get_info, "")
        username = re.search(
            Server_socket.field_username.replace("{}", "(.*?)"),
            recog).groups(0)
        username = username[0]

        if not self.users_chats.__contains__(username):
            self.users_chats[username] = deque()
            self.users_chats[username].append(
                "connected to Server. You can ready chat\n")

        def not_for_this_user(dicct):
            for key in dicct.keys():
                if not key.__eq__(username):
                    dicct[key] = None
            return dicct

        send_to_client = not_for_this_user(self.users_chats.copy())
        # send_to_client[Chat_server.field_change_user]=deque(["NULL"])

        return Server_socket.serialize_object(send_to_client)

    def new_message(self, msg_obj: MessagePattern):
        if not self.users_chats.__contains__(msg_obj.from_user):
            self.users_chats[msg_obj.from_user] = deque()
        if not self.users_chats.__contains__(msg_obj.to_user):
            self.users_chats[msg_obj.to_user] = deque()

        print(msg_obj)

        self.users_chats.get(msg_obj.from_user).append(msg_obj)
        self.users_chats.get(msg_obj.to_user).append(msg_obj)

    def send_answer_bytes_chat(self, context_super, conn, data):
        try:
            string_comand = data.decode()
            if string_comand.__contains__(Server_socket.field_get_info):
                status_for_client = self.send_info_data_to_client(
                    string_comand)
                context_super.send(conn, status_for_client)
                return True
        except UnicodeDecodeError as er:
            dd=0

        return False

    def override_socket_need_data_collect(self):
        def new_check_data_need_storage(self,data):
            try:
                obj = pickle.loads(data)

                if type(obj).__name__ is "MessagePattern":
                    return True
            except:
                sad=0

            return False


        self.module_server_socket.check_data_need_storage = types.MethodType(
            new_check_data_need_storage, self.module_server_socket)


if __name__ == '__main__':
    chat_server = Chat_server()
