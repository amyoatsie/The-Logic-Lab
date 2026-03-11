import tkinter as tk                                    
from tkinter import ttk
#don't fully understand

class SummaryScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ------------------------
        # Tabs
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=(5,10))

        ttk.Button(nav_frame, text="Main", command=lambda: app.show_frame("InventoryScreen")).pack(side="left", padx=5)

        ttk.Button(nav_frame, text="Summary", command=lambda: app.show_frame("SummaryScreen")).pack(side="left", padx=5)

        # ------------------------
        # Title
        ttk.Label(self, text="Inventory Summary", font=("Segoe UI",16,"bold")).pack(pady=20)

        # ------------------------
        # Summary Display
        self.summary_label = ttk.Label(self, font=("Segoe UI",11), justify="left")
        self.summary_label.pack(pady=20)

    # ------------------------
    # Calculate totals and display
    def refresh_summary(self):

        inventory_screen = self.app.frames["InventoryScreen"]

        category_totals = {}
        total_value = 0

        for item in inventory_screen.items:

            category = item["category"]
            qty = int(item["quantity"])
            price = float(item["price"])

            # total stock per category
            category_totals[category] = category_totals.get(category, 0) + qty

            # total value
            total_value += qty * price

        # ------------------------
        # Format display text
        text = "Stock Per Category\n"
        text += "----------------------\n"

        for cat, qty in category_totals.items():
            text += f"{cat}: {qty}\n"

        text += "\n"
        text += "----------------------\n"
        text += f"Total Inventory Value: ${total_value:.2f}"

        self.summary_label.config(text=text)