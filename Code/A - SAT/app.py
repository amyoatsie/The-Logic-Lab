import tkinter as tk
from pathlib import Path

#import repos testing
#import screens

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("User Module Access")
        self.root.geometry("720x460")

        #variables defined inside app class, therefore references as "app.___"
        base_dir = Path(__file__).resolve().parent #references the "relative folder"!!!
        data_dir = base_dir / "data" #act like global variables but are only defined once

        #define repos
        #define screens
        #define other app vars such as user

#write navigation functions

def run(self):#method for mainloop
    self.root.mainloop()