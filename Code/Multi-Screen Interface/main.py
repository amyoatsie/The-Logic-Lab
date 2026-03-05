import tkinter as tk
from inventory_screen import InventoryScreen
from summary_screen import SummaryScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Manager")
        self.geometry("950x450")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F, name in [(InventoryScreen,"InventoryScreen"), (SummaryScreen,"SummaryScreen")]:
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InventoryScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if name == "SummaryScreen":
            frame.refresh_summary()

if __name__ == "__main__":
    app = App()
    app.mainloop()