import tkinter as tk
from tkinter import ttk

from repos.task_repo_csv import TaskRepoCsv
from screens.tasks_screen import TasksScreen
from screens.dashboard_screen import DashboardScreen


class App:
    def __init__(self):
        self.repo = TaskRepoCsv()
        self.tasks = self.repo.load_all()

        self.root = tk.Tk() #the variable root contains an instance of the tkinter class
        #but self. is OOP, which refers to self in memory so it knows this particular insance of the class
        #avoids the instruction branching out
        self.root.title("Homework Tracker")
        self.root.geometry("1150x560")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        outer = ttk.Frame(self.root, padding=12)
        outer.grid(row=0, column=0, sticky=tk.NSEW)

        outer.rowconfigure(1, weight=1)
        outer.columnconfigure(0, weight=1)

        nav = ttk.Frame(outer)
        nav.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))

        ttk.Button(nav, text="Tasks", command=lambda: self.show_screen("tasks")).grid( #always use self. to call variables
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(nav, text="Dashboard", command=lambda: self.show_screen("dashboard")).grid(
            row=0,
            column=1,
            padx=(0, 8),
        )

        content = ttk.Frame(outer)
        content.grid(row=1, column=0, sticky=tk.NSEW)

        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        self.screens = {} #dictionary

        self.screens["tasks"] = TasksScreen(content, self)
        self.screens["tasks"].grid(row=0, column=0, sticky=tk.NSEW) #screen 1

        self.screens["dashboard"] = DashboardScreen(content, self)
        self.screens["dashboard"].grid(row=0, column=0, sticky=tk.NSEW) #screen 2

        self.show_screen("tasks") #starting screen

    def show_screen(self, name):
        frame = self.screens.get(name)
        if frame is None:
            return

        frame.tkraise()

        if name == "dashboard":
            self.refresh_dashboard()

    def refresh_dashboard(self):
        dash = self.screens.get("dashboard")
        if dash is None:
            return
        dash.refresh()

    def save(self):
        self.repo.save_all(self.tasks)

    def run(self):
        self.root.mainloop()