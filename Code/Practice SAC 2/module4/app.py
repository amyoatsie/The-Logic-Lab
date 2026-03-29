import tkinter as tk
from pathlib import Path
from datetime import date
from screens.order_screen import OrderScreen
from repos.order_repo import OrderRepo

class App:
    def __init__(self): #the main section at the bottom of module 3
        self.root = tk.Tk()
        self.root.title("Beebay - Module 4")
        self.root.geometry("700x420")

        today = date.today() #refence totdays date for csv file title
        base_dir = Path(__file__).resolve().parent  #module 3 __init__ section
        data_file = base_dir / "data" / f"{today}sales.csv" #references the csv by going into the "data" folder
        
        self.order_repo = OrderRepo(data_file) #calls the orderRepo function?
        OrderScreen(self.root, self.order_repo)

    def run(self):
        self.root.mainloop() #ALWAYS INCLUDE