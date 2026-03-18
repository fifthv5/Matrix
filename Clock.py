from tkinter import *
from tkinter.ttk import *
import os

def clear():
    os.system("clear")
from time import strftime

root = Tk()
root.title("Clock")

def time():
    string = strftime("%I:%M:%S %p")
    label.config(text=string)
    label.after(1000, time)

label = Label(root, font=("ds-digital", 80),background="black", foreground="cyan")
label.pack(anchor="center")
time()

mainloop()
