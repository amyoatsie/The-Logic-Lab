import tkinter as tk
from tkinter import ttk, messagebox
from inventory_repo import load_inventory, save_inventory

class InventoryScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ------------------------
        # Style :)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TFrame", background="#edd0f1")
        style.configure("Custom.TLabel", background="#edd0f1", foreground="#222")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=25)
        style.map("Treeview", background=[("selected", "#ff4ff3")])
        style.configure("Treeview.Heading", background="#502350", foreground="white", font=("Segoe UI", 10, "bold"))

        # ------------------------
        # Main container frame
        frame = ttk.Frame(self, padding=12, style="Custom.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=2)
        frame.rowconfigure(6, weight=1)

        # ------------------------
        # Tab buttons at top for the multi-page bit
        nav_frame = ttk.Frame(frame, style="Custom.TFrame")
        nav_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0,10))
        ttk.Button(nav_frame, text="Main", command=lambda: app.show_frame("InventoryScreen")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Summary", command=lambda: app.show_frame("SummaryScreen")).pack(side="left", padx=5)

        # ------------------------
        # Variables
        self.item_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Hat") #for preset
        self.price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()

        # ------------------------
        # Labels
        labels = ["Item ID", "Name", "Category", "Price", "Quantity"]
        for i, text in enumerate(labels):
            ttk.Label(frame, text=text, style="Custom.TLabel").grid(row=i+1, column=0, sticky="w", pady=6)

        # ------------------------
        # Entry widgets (kinda the same)
        self.entry_id = ttk.Entry(frame, textvariable=self.item_id_var)
        self.entry_id.grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Entry(frame, textvariable=self.name_var).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Combobox(frame, textvariable=self.category_var, values=["Hat","Shirt","Pants"], state="readonly").grid(row=3, column=1, sticky="ew", pady=6)
        ttk.Entry(frame, textvariable=self.price_var).grid(row=4, column=1, sticky="ew", pady=6)
        ttk.Entry(frame, textvariable=self.quantity_var).grid(row=5, column=1, sticky="ew", pady=6)

        # ------------------------
        # Buttons
        ttk.Button(frame, text="Add", command=self.add_item).grid(row=6, column=1, sticky="ew", pady=(10,0))
        ttk.Button(frame, text="Save Inventory", command=self.save_items).grid(row=6, column=0, sticky="ew", pady=(10,0))

        # ------------------------
        # Treeview (styled) :)
        self.tree = ttk.Treeview(frame, columns=("id","name","category","price","quantity"), show="headings", height=12)
        for col in ("id","name","category","price","quantity"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=1, column=3, rowspan=6, sticky="nsew", padx=(12,0))
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#ebdaf0")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ------------------------
        # Load inventory
        self.items = load_inventory()
        self.refresh_tree()
        self.entry_id.focus_set()

    # ------------------------
    # Treeview and form methods
    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, item in enumerate(self.items):
            tag = "even" if index % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(item["id"], item["name"], item["category"], item["price"], item["quantity"]), tags=(tag,))

    def on_select(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.item_id_var.set(values[0])
        self.name_var.set(values[1])
        self.category_var.set(values[2])
        self.price_var.set(values[3])
        self.quantity_var.set(values[4])

    def add_item(self):
        try:
            item_id = int(self.item_id_var.get())
            if any(it["id"] == item_id for it in self.items):
                messagebox.showerror("Duplicate ID","This Item ID already exists")
                return
            name = self.name_var.get().strip()
            category = self.category_var.get().strip()
            price = float(self.price_var.get())
            quantity = int(self.quantity_var.get())
            if not name:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input","Check all fields are valid")
            return

        self.items.append({
            "id": item_id,
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity
        })
        self.refresh_tree()
        self.clear_form()

    def clear_form(self):
        self.item_id_var.set("")
        self.name_var.set("")
        self.category_var.set("Hat")
        self.price_var.set("")
        self.quantity_var.set("")
        self.entry_id.focus_set()

    def save_items(self):
        save_inventory(self.items)
        messagebox.showinfo("Saved","Inventory saved successfully")