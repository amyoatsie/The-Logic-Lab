import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent #relative path, resolve gives the full path, parent gives the folder
CSV_PATH = BASE_DIR / "sales.csv" #CONSTANTS, must be added
CSV_FIELDS = ["sale_id", "num_workers" , "num_queens", "distance_km", "bonus_code", "final_cost"]

def ensure_csv_exists(): #a function to ensure the csv file exists to prevent crashes
    if CSV_PATH.exists() is True:
        return

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

def load_tasks():
    ensure_csv_exists()

    tasks = []
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("sale_id", "").isdigit() is False:
                continue

            tasks.append(
                {
                    "sale_id": int(row["Sale Id"]),
                    "num_workers": int(row.get("workers", "")),
                    "num_queens": int(row.get("queens", "")),
                    "distance_km": row.get("Distance (km)", ""),
                    "bonus_code": row.get("Bonus Code", ""),
                    "final_cost": row.get("Final Cost", ""),
                }
            )
    return tasks

def save_tasks(tasks): #calls & runs the ensure_csv_exists function at the start
    ensure_csv_exists()

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for task in tasks:
            writer.writerow(
                {
                    "sale_id": str(task["sale_id"]),
                    "num_workers": task["num_workers"],
                    "num_queens": task["num_queens"],
                    "distance_km": task["distance_km"],
                    "bonus_code": task["bonus_code"],
                    "final_cost": task["final_cost"],
                }
            )


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
        

        # ToDo: implement search and filter code
        # 1. load file for reading
        # 2. add matching rows to a list
        # 3. sort matching list
        # 4. load list to treeview
        #  - do you need multiple functions? 

        #list = [] #why is the text pink???
        pass


def main():

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")

    BeeBayAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()