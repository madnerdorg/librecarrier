from tkinter import *
from threading import Thread
import sys
import os
import socket
from twisted.internet import reactor
from tkinter import ttk
from modules import Settings
global args
args = Settings.get()


def quit():
    reactor.stop()


def goToWeb():
    global args
    os.system("explorer " + args["web_url"])


def goToSettings():
    os.system("explorer settings")


def gui():
    global args
    # Create interface
    bg_grey = "#f3f3f3"
    root = Tk()
    try:
        root.iconbitmap('libreCarrier.ico')
    except:
        pass
    root.title("Libre Carrier")  #Title
    root.configure(background=bg_grey)  #Background color
    root.protocol("WM_DELETE_WINDOW", quit)

    ent = ttk.Entry(root, state='readonly')
    var = StringVar()
    var.set(args["web_url"])
    ent.config(textvariable=var, width=50,justify='center')
    ent.pack()

    ttk.Button(text="Exit", command=quit, width=50).pack()
    ttk.Button(text="Web", command=goToWeb, width=50).pack()
    ttk.Button(text="Settings", command=goToSettings, width=50).pack()
    root.mainloop()


gui_thread = Thread(target=gui)
gui_thread.daemon = True  # If thread is not a daemon application could crashed
gui_thread.start()
