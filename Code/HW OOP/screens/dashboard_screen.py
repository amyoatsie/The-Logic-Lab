import tkinter as tk
from tkinter import ttk

from models.task import is_valid_date
from models.task import to_date


class DashboardScreen(ttk.Frame): #frame is the parent
    def __init__(self, parent, app): #as screen is inside of frame which is inside of screen
                                    #so innermost thing (screen) must be told what it relates to
        super().__init__(parent) #calls super because dashboard is part of ttk so must repeat all of this
        self.app = app

        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Dashboard", font=("Segoe UI", 12, "bold")).grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=(0, 12),
        )

        self.lbl_total = ttk.Label(self, text="")
        self.lbl_total.grid(row=1, column=0, sticky=tk.W, pady=6)

        self.lbl_pending = ttk.Label(self, text="")
        self.lbl_pending.grid(row=2, column=0, sticky=tk.W, pady=6)

        self.lbl_done = ttk.Label(self, text="")
        self.lbl_done.grid(row=3, column=0, sticky=tk.W, pady=6)

        self.lbl_overdue = ttk.Label(self, text="")
        self.lbl_overdue.grid(row=4, column=0, sticky=tk.W, pady=6)

        self.lbl_next_due = ttk.Label(self, text="")
        self.lbl_next_due.grid(row=5, column=0, sticky=tk.W, pady=6)

        self.refresh()

    def refresh(self):
        import datetime

        total = len(self.app.tasks)
        pending = len([t for t in self.app.tasks if t.status == "Pending"])
        done = len([t for t in self.app.tasks if t.status == "Done"])

        today = datetime.date.today()
        overdue = 0

        for t in self.app.tasks:
            if t.status == "Done":
                continue
            if is_valid_date(t.due_date) is False:
                continue
            if to_date(t.due_date) < today:
                overdue += 1

        next_due_text = "Next due: (none)"
        pending_tasks = []

        for t in self.app.tasks:
            if t.status != "Pending":
                continue
            if is_valid_date(t.due_date) is False:
                continue
            pending_tasks.append(t)

        pending_tasks.sort(key=lambda x: to_date(x.due_date))

        if len(pending_tasks) > 0:
            t = pending_tasks[0]
            next_due_text = f"Next due: {t.due_date} ({t.subject})"

        self.lbl_total.config(text=f"Total tasks: {total}")
        self.lbl_pending.config(text=f"Pending: {pending}")
        self.lbl_done.config(text=f"Done: {done}")
        self.lbl_overdue.config(text=f"Overdue (pending only): {overdue}")
        self.lbl_next_due.config(text=next_due_text)