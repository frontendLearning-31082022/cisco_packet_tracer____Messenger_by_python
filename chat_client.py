import _pickle
import ctypes
import pickle
import socket
import sys
import time
import types
from threading import Timer
from tkinter import END

from chat_server import MessagePattern, Chat_server
from structure.client_socket import Client_socket
from structure.encryption.RSA.client_socket_RSA import Client_socket_RSA
from structure.gui_chat import Gui_chat
from structure.server_socket import Server_socket
from structure.window_info import Window_info


class Chat_client:
    def __init__(self):

        self.username = Window_info.show_input("Введите ваше имя")
        if self.username == None:
            sys.exit()

        self.all_data=None

        self.ip = socket.gethostbyname(socket.gethostname())
        self.gui = Gui_chat(username=self.username,title=f'Client {self.username} {self.ip}',path_icon=
                            "structure/icons/client.png",)

        self.gui.start()

        time.sleep(3)
        self.gui.button_send.config(command=self.send_to_server)
        # self.module_client_socket = Client_socket(self.ip, 7777)
        self.module_client_socket = Client_socket_RSA(self.ip, 7777)

        while True:
            self.listen_server_updates()
            time.sleep(3)

    # def send_button_override(self):
    #     def new_listener_button():
    #         safg
    #         self.module_client_socket.send_echo("")
    #
    #     self.gui.send_button_listener=types.MethodType(new_listener_button,self.gui)


    def send_to_server(self):
        send_to= self.gui.name_choosed_to_send.get()

        if send_to.__eq__(Gui_chat.field_not_choosed_sender):
            ctypes.windll.user32.MessageBoxW(0, "Выберите получателя", "Error",0)
            return

        msg = MessagePattern(from_user=self.username, to_user=send_to,
                             message=self.gui.input_message.get("1.0", END))
        serialized = Server_socket.serialize_object(msg)

        success= self.module_client_socket.send_echo_object(serialized)
        if not success:
            ctypes.windll.user32.MessageBoxW(0, "Сервер не принял соорбщение", "Error",
                                             0)
            return


    def listen_server_updates(self):
        try:
           status_from_server=self.module_client_socket.send_answer_get(
                f"{Server_socket.field_get_info}" + Server_socket.field_username.format(
                    self.username))

           data_recog = dict(pickle.loads(status_from_server))
           self.all_data=data_recog
           self.gui.refresh(self.all_data)
           asd=0
        except Exception as exc:
            pass


# self.gui.input_message

if __name__ == '__main__':
    chat_client = Chat_client()
