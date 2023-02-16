# Напишите свою программу сервер и запустите её.
# Запустите несколько клиентов. Сымитируйте чат.
import time
import tkinter
from abc import abstractmethod
from collections import deque
from threading import Thread
from tkinter import Tk, Text, DISABLED, Frame, Canvas, X, Button, RIGHT, END
from tkinter.ttk import Label
import ctypes as ct


class Gui_chat(Thread):
    field_not_choosed_sender="выберите получателя"

    def gui_generate(self):
        title = self.title
        path_icon = self.path_icon

        self.window = Tk()
        self.window.title(title)
        self.window.geometry("850x450")

        self.chat_tree = Text(self.window, height=18, width=100)
        self.chat_tree.config(foreground='white')
        self.chat_tree.config(background="#1a1a4d")
        self.chat_tree.config(state='normal')
        self.chat_tree.pack()
        self.chat_tree.insert('end', 'waiting connect to server')
        self.chat_tree.config(state=DISABLED)
        self.chat_tree.delete(1.0, "end")
        self.input_message = Text(self.window, height=5, width=100)
        self.input_message.config(state='normal')
        self.input_message.pack()
        self.input_message.insert('end', 'enter msg here')

        self.name_choosed_to_send = tkinter.StringVar(self.window)
        self.name_choosed_to_send.set(Gui_chat.field_not_choosed_sender)
        self.select_user_to = tkinter.OptionMenu(self.window, self.name_choosed_to_send,
                                                 "только один клиент в сети")
        self.select_user_to.pack()

        self.button_send = Button(self.window, text="Отправить", height=10,
                                  width=50)

        self.button_send.pack(side=RIGHT)

        if path_icon != None:
            try:
                self.window.iconphoto(False, tkinter.PhotoImage(
                    file=path_icon))
            except:
                pass
        self.window.mainloop()

    def __init__(self, title, username, path_icon=None):
        Thread.__init__(self)
        self.title = title
        self.path_icon = path_icon
        self.username = username

    def run(self):
        self.gui_generate()

    # @abstractmethod
    # def send_button_listener(self):
    #     hello_opp=0




    def tree_char_set(self, value):
        self.chat_tree.config(state='normal')
        self.chat_tree.delete(1.0, "end")
        self.chat_tree.insert("end", value)
        self.chat_tree.config(state=DISABLED)

    def refresh(self, all_data):
        new_chat = deque( dict(all_data)[self.username])



        # easy way
        self.chat_tree.config(state='normal')
        self.chat_tree.delete('1.0', END)
        for string in new_chat:
            self.chat_tree.insert('end', string)
        self.chat_tree.config(state=DISABLED)

        names = dict(all_data).keys()
        names = set(names)
        names.remove(self.username)
        if len(names) == 0:
            names.add("один пользователь в сети")

        if len(names) > 0:
            menu = self.select_user_to["menu"]
            menu.delete(0, "end")

            for string in names:
                menu.add_command(label=string,
                                 command=lambda
                                     value=string: self.name_choosed_to_send.set(value))

            # self.select_user_to = tkinter.OptionMenu(self.window,
            #                                          self.variable,
            #                                          "names")
            self.select_user_to.pack()

        pass
