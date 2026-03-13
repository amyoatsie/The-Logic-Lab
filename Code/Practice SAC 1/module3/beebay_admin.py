import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv


class BeeBayAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        #sets the starting value of the variables for the dropdown/"comboboxes"
        self.filter_var = tk.StringVar(value="Orders with queens")
        self.sort_var = tk.StringVar(value="total_cost")

        self.setup_grid()
        self.create_widgets()

        #define CSV file location (in this case within the same folder)
        BASE_DIR = Path(__file__).resolve().parent
        self.sales_csv = BASE_DIR / "sales.csv"

    def setup_grid(self): #configures the main layout

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        lbl_heading = ttk.Label(self, text="BeeBay Admin", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        #filter label and combobox/dropdown
        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly", #prevents the user attempting to alter the options
            values=["Orders with queens", "Orders with no queens"]
        )
        cbo_filter.grid(row=1, column=1, sticky="ew", pady=5)

        #sort label and combobox/dropdown
        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["total_cost", "distance_km"]
        )
        cbo_sort.grid(row=2, column=1, sticky="ew", pady=5)

        #button to load treeview
        btn_go = ttk.Button(self, text="Load Results", command=lambda: self.load_results())
        btn_go.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=5)

        #actual treeview to display results
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

        #adds a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)

#-----------------------------------
    def read_sales_file(self):
        rows = [] #creates an empty list
        try:
            with open(self.sales_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #converts numeric fields
                    row["num_queens"] = int(row["num_queens"])
                    row["final_cost"] = float(row["final_cost"])
                    row["distance_km"] = float(row["distance_km"])
                    rows.append(row) #adds the numeric fields to the empty list
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.sales_csv}")
        return rows #returns the empty list and prevents program from crashing

    def filter_sales(self, rows): #function to filter rows based on the selected filter
        filtered = [] #creates an empty list for the new filtered rows to be appended within
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "Orders with queens" and row["num_queens"] > 0:
                filtered.append(row) #adds each row which meets the criteria to the list
            elif filter_option == "Orders with no queens" and row["num_queens"] == 0:
                filtered.append(row)
        return filtered

    def sort_sales(self, rows):
        sort_option = self.sort_var.get()
        if sort_option == "total_cost": #sorts result list by final cost
            return sorted(rows, key=lambda x: x["final_cost"]) #simplified version of list creation to reduce redundincy
        else: #as there are currently only two sorting options, if it isn't one it will default to the other
            return sorted(rows, key=lambda x: x["distance_km"])

    def display_sales(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clears existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["sale_id"], 
                                                row["num_workers"], 
                                                row["num_queens"],
                                                row["distance_km"]
                                                row["bonus_code"],
                                                row["final_cost"]
                                                ))



    def load_results(self): #main function
        rows = self.read_sales_file() #read CSV/'load file for reading'
        if not rows: #provides an escape path to prevent crashes, stopping if file is not found
            return
        rows = self.filter_sales(rows) #filters list
        rows = self.sort_sales(rows) #sorts list
        self.display_sales(rows) #loads list to treeview and displays data
    
        # ToDo: implement search and filter code
        # 1. load file for reading
        # 2. add matching rows to a list
        # 3. sort matching list
        # 4. load list to treeview
        #  - do you need multiple functions? 
        pass


def main():

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")

    BeeBayAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()