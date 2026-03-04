import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

from models.task import Task
from models.task import is_valid_date
from models.task import to_date


class TasksScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.id_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pending")
        self.filter_var = tk.StringVar(value="All")

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=2)
        self.rowconfigure(10, weight=1)

        ttk.Label(self, text="Tasks", font=("Segoe UI", 12, "bold")).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=tk.W,
            pady=(0, 10),
        )

        ttk.Label(self, text="ID").grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(self, text="Subject").grid(row=2, column=0, sticky=tk.W, pady=6)
        ttk.Label(self, text="Description").grid(row=3, column=0, sticky=tk.W, pady=6)
        ttk.Label(self, text="Due date (YYYY-MM-DD)").grid(row=4, column=0, sticky=tk.W, pady=6)
        ttk.Label(self, text="Status").grid(row=5, column=0, sticky=tk.W, pady=6)
        ttk.Label(self, text="View").grid(row=7, column=0, sticky=tk.W, pady=(18, 6))

        self.entry_id = ttk.Entry(self, textvariable=self.id_var, state="readonly")
        self.entry_id.grid(row=1, column=1, sticky=tk.EW, pady=6)

        ttk.Entry(self, textvariable=self.subject_var).grid(row=2, column=1, sticky=tk.EW, pady=6)

        self.entry_desc = ttk.Entry(self, textvariable=self.desc_var)
        self.entry_desc.grid(row=3, column=1, sticky=tk.EW, pady=6)

        ttk.Entry(self, textvariable=self.due_date_var).grid(row=4, column=1, sticky=tk.EW, pady=6)

        self.combo_status = ttk.Combobox(
            self,
            textvariable=self.status_var,
            values=["Pending", "Done"],
            state="readonly",
        )
        self.combo_status.grid(row=5, column=1, sticky=tk.EW, pady=6)

        self.filter_combo = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            values=["All", "Pending", "Done", "Overdue"],
            state="readonly",
        )
        self.filter_combo.grid(row=7, column=1, sticky=tk.EW, pady=(18, 6))

        self.tree = ttk.Treeview(
            self,
            columns=("id", "subject", "due", "status"),
            show="headings",
            height=16,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("due", text="Due Date")
        self.tree.heading("status", text="Status")
        self.tree.grid(row=0, column=3, rowspan=11, sticky=tk.NSEW, padx=(12, 0))

        ttk.Button(self, text="Add", command=self.add_task).grid(
            row=8,
            column=0,
            sticky=tk.EW,
            pady=(10, 0),
        )
        ttk.Button(self, text="Update", command=self.update_task).grid(
            row=8,
            column=1,
            sticky=tk.EW,
            pady=(10, 0),
        )
        ttk.Button(self, text="Delete", command=self.delete_task).grid(
            row=9,
            column=0,
            columnspan=2,
            sticky=tk.EW,
            pady=6,
        )

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.filter_combo.bind("<<ComboboxSelected>>", self.on_filter_change)

        self.refresh_view()
        self.clear_form()

    def _apply_filter(self, tasks, mode):
        if mode == "All":
            return list(tasks)

        if mode == "Pending":
            return [t for t in tasks if t.status == "Pending"]

        if mode == "Done":
            return [t for t in tasks if t.status == "Done"]

        if mode == "Overdue":
            today = datetime.date.today()
            overdue = []

            for t in tasks:
                if t.status == "Done":
                    continue
                if is_valid_date(t.due_date) is False:
                    continue
                if to_date(t.due_date) < today:
                    overdue.append(t)

            return overdue

        return list(tasks)

    def _sort_by_due_date(self, tasks):
        def key_func(t):
            if is_valid_date(t.due_date) is False:
                return datetime.date.max
            return to_date(t.due_date)

        return sorted(tasks, key=key_func)

    def refresh_tree(self, visible_tasks):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for t in visible_tasks:
            self.tree.insert(
                "",
                tk.END,
                values=(t.id, t.subject, t.due_date, t.status),
            )

    def refresh_view(self):
        visible = self._apply_filter(self.app.tasks, self.filter_var.get())
        visible = self._sort_by_due_date(visible)
        self.refresh_tree(visible)

    def clear_form(self):
        next_id = self.app.repo.get_next_id(self.app.tasks)

        self.id_var.set(next_id)
        self.subject_var.set("")
        self.desc_var.set("")
        self.due_date_var.set("")
        self.status_var.set("Pending")

    def validate_common(self):
        subject = self.subject_var.get().strip()
        desc = self.desc_var.get().strip()
        due = self.due_date_var.get().strip()

        if subject == "":
            messagebox.showerror("Invalid", "Subject is required.")
            return False

        if desc == "":
            messagebox.showerror("Invalid", "Description is required.")
            return False

        if is_valid_date(due) is False:
            messagebox.showerror("Invalid", "Due date must be YYYY-MM-DD.")
            return False

        return True

    def add_task(self):
        ok = self.validate_common()
        if ok is False:
            return

        task_id = int(self.id_var.get())

        new_task = Task(
            id=task_id,
            subject=self.subject_var.get().strip(),
            description=self.desc_var.get().strip(),
            due_date=self.due_date_var.get().strip(),
            status=self.status_var.get().strip(),
        )

        self.app.repo.add(self.app.tasks, new_task)

        self.refresh_view()
        self.clear_form()
        self.app.refresh_dashboard()

    def update_task(self):
        selected = self.tree.selection()
        if len(selected) == 0:
            messagebox.showinfo("Select", "Select a task in the table first.")
            return

        ok = self.validate_common()
        if ok is False:
            return

        values = self.tree.item(selected[0], "values")
        task_id = int(values[0])

        updated_task = Task(
            id=task_id,
            subject=self.subject_var.get().strip(),
            description=self.desc_var.get().strip(),
            due_date=self.due_date_var.get().strip(),
            status=self.status_var.get().strip(),
        )

        ok_update = self.app.repo.update(self.app.tasks, updated_task)
        if ok_update is False:
            messagebox.showinfo("Not found", "No matching task to update.")
            return

        self.refresh_view()
        self.app.refresh_dashboard()

    def delete_task(self):
        selected = self.tree.selection()
        if len(selected) == 0:
            messagebox.showinfo("Select", "Select a task in the table first.")
            return

        values = self.tree.item(selected[0], "values")
        task_id = int(values[0])

        ok_delete = self.app.repo.delete(self.app.tasks, task_id)
        if ok_delete is False:
            return

        self.refresh_view()
        self.clear_form()
        self.app.refresh_dashboard()

    def on_select(self, event=None):
        selected = self.tree.selection()
        if len(selected) == 0:
            return

        values = self.tree.item(selected[0], "values")
        task_id = int(values[0])

        self.id_var.set(task_id)
        self.subject_var.set(values[1])
        self.due_date_var.set(values[2])
        self.status_var.set(values[3])

        self.desc_var.set("")
        for t in self.app.tasks:
            if t.id == task_id:
                self.desc_var.set(t.description)
                return

    def on_filter_change(self, event=None):
        self.refresh_view()