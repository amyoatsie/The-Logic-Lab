import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv
CSV_PATH = "sales.csv"

def load_results():
    try: #must exist or will crash
        with open(CSV_PATH, newline="", encoding="utf-8") as tasks_file:
            temp = []
            for row in csv.DictReader(tasks_file):
                temp.append({
                    "sale_id": int(row["sale_id"]),
                    "num_workers": int(row["num_workers"]),
                    "num_queens": int(row["num_queens"]),
                    "distance_km": float(row["distance_km"]),
                    "bonus_code": (row["bonus_code"]),
                    "final_cost": float(row["final_cost"]),
                })
            return temp
    
    except FileNotFoundError: #if doesn't exist, this recovers the program rather than crashing
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f: #w is important as it WRITES
            w = csv.DictWriter(f, fieldnames=["sale_id", "num_workers" , "num_queens", "distance_km", "bonus_code", "final_cost"])
            w.writeheader()
            return[] #returns an empty LIST

def save_results(tasks):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sale_id", "num_workers" , "num_queens", "distance_km", "bonus_code", "final_cost"])
        w.writeheader()
        for task in tasks:
            w.writerow({
                "sale_id": task["sale_id"],
                "num_workers": task["num_workers"],
                "num_queens": task["num_queens"],
                "distance_km": task["distance_km"],
                "bonus_code": task["bonus_code"],
                "final_cost": task["final_cost"],
            })

def refresh_tree(tree, tasks):
    """Clears and repopulates the Treeview with tasks from the list."""
    for i in tree.get_children():
        tree.delete(i)


    for index, s in enumerate(tasks): #styling of colour formats
        tag = "even" if index % 2 == 0 else "odd" #helps with colouring
        tree.insert("", tk.END,
                values=(s["sale_id"], s["num_workers"], s["num_queens"], s["distance_km"], s["bonus_code"], s["final_cost"]), #table columns
                tags=(tag,)) #allows you to change the row colours


#-------------------------

class BeeBayAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="Orders with queens")
        self.sort_var = tk.StringVar(value="total_cost")

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.sales_csv = BASE_DIR / "sales.csv"

    def setup_grid(self):

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        lbl_heading = ttk.Label(self, text="BeeBay Admin", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=["Orders with queens", "Orders with no queens"]
        )
        cbo_filter.grid(row=1, column=1, sticky="ew", pady=5)

        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["total_cost", "distance_km"]
        )
        cbo_sort.grid(row=2, column=1, sticky="ew", pady=5)

        #allows the table to auto update
        #cbo_filter.bind("<<ComboboxSelected>>", lambda e: self.load_results())
        #cbo_sort.bind("<<ComboboxSelected>>", lambda e: self.load_results())

        btn_go = ttk.Button(self, text="Load Results", command=lambda: self.load_results())
        btn_go.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=5)

        columns = (
            "sale_id",
            "num_workers",
            "num_queens",
            "distance_km",
            "bonus_code",
            "final_cost"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        headings = {
            "sale_id": "Sale ID",
            "num_workers": "Workers",
            "num_queens": "Queens",
            "distance_km": "Distance (km)",
            "bonus_code": "Bonus Code",
            "final_cost": "Final Cost"
        }

        widths = {
            "sale_id": 90,
            "num_workers": 90,
            "num_queens": 90,
            "distance_km": 120,
            "bonus_code": 120,
            "final_cost": 100
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def load_results(self):
        tasks = load_results()

        results = []

        if self.filter_var.get() == "Orders with queens":
            results = [t for t in tasks if t["num_queens"] > 0]
        else:
            results = [t for t in tasks if t["num_queens"] == 0]

        if self.sort_var.get() == "distance_km":
            results.sort(key=lambda x: x["distance_km"])
        else:
            results.sort(key=lambda x: x["final_cost"])

        # Convert floats to strings for display
        for t in results:
            t["distance_km"] = str(t["distance_km"])
            t["final_cost"] = str(t["final_cost"])

        refresh_tree(self.tree, results)


def main():

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")
    BeeBayAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()