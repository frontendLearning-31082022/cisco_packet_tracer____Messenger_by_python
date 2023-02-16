import sys
import tkinter
from ctypes import windll
from ctypes.wintypes import POINT
from tkinter import *
from tkinter import ttk

from _ctypes import byref


class Window_info:
    @staticmethod
    def callback(input_field, master, res):
        # print(input_field.get())
        res.add(input_field.get())
        master.destroy()

    @staticmethod
    def on_closing():
        sys.exit()

    @staticmethod
    def show_input(msg):
        result = set()

        master = Tk()

        master.eval('tk::PlaceWindow . center')
        master.geometry("250x200")

        label = ttk.Label(text=msg, font=("Arial", 14))
        label.pack()

        e = tkinter.Entry(master, width=20)
        e.pack()
        e.focus_set()

        master.bind('<Return>',
                    lambda t: Window_info.callback(e, master, result))


        b = Button(master, text="OK", width=20,
                   command=lambda: Window_info.callback(e, master, result))
        b.pack()

        master.protocol("WM_DELETE_WINDOW", Window_info.on_closing)
        mainloop()
        return list(result)[0]
