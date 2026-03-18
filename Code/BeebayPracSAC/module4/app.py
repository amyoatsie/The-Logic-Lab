import tkinter as tk
from pathlib import Path
from datetime import date
from screens.order_screen import OrderScreen
from repos.order_repo import OrderRepo

class App:
    def __init__(self): #constructor (the __int__ method of the class), automatically called when you create an instance
        self.root = tk.Tk() #DONT FORGET SELF.
        self.root.title("Beebay - Module 4")
        self.root.geometry("700x420")

        today = date.today() #assigns the built in "date." static method to the var 'today' T(as indicated by the .) HIS WILL BE IMPORTANT!!!
        base_dir = Path(__file__).resolve().parent #resolve is a method as indicated by the . and (), parent is an attribute as it doesn't havee ()
        data_file = base_dir / "data" / f"{today}sales.csv"
        
        self.order_repo = OrderRepo(data_file) #creates an instance of the order repo
        OrderScreen(self.root, self.order_repo) #create an instance of the order screen

    def run(self):
        self.root.mainloop()
