import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv 
'''sources data from a CSV file as it is explicitly stated within the design brief and as alternate data types would not function 
as well (txt data is not structured enough and XML is over complicated for the programs given requirements) :)'''

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
            state="readonly", #prevent the user attempting to alter the options
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

        #titles of columns in the actual treeview to display results
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
    def read_sales_file(self): #function to read all of the CSV files and format them into a new list 'rows'
        rows = [] #create an empty list to append the relevant data which can be used for filtering/sorting
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        try:
            with open(self.sales_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["num_queens"] = int(row["num_queens"]) #convert num_queens to an integer as it must be a whole number
                    row["final_cost"] = float(row["final_cost"]) #convert final_cost to a float as it may be a decimal number
                    row["distance_km"] = float(row["distance_km"]) #convert distance_km to a float as it may be a decimal number
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.sales_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found

    def filter_sales(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "Orders with queens" and row["num_queens"] > 0:
                #add each CSV row to the new filtered list which meets the selected filter criteria of at least 1 queen
                filtered.append(row)
            elif filter_option == "Orders with no queens" and row["num_queens"] == 0:
                #add     each CSV row to the new filtered list which meets the selected filter criteria of 0 queens
                filtered.append(row)
            
            #ToDo: add a filter 'All' to display all csv data
        return filtered #exit function and pass out the new filtered list

    def sort_sales(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_var.get() #find the selected dropdown for sort by
        
        if sort_option == "total_cost": #sort result list by final cost
            return sorted(rows, key=lambda x: x["final_cost"]) #simplified version of list creation to reduce redundincy
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        else: #as there are currently only two sorting options, if it isn't one it will default to the other
            #ToDo: if more sorting options were added this must be changed to an elif statement
            return sorted(rows, key=lambda x: x["distance_km"])
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        #ToDo: add a sorting function to sort by Sale ID

    def display_sales(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["sale_id"], 
                                                row["num_workers"], 
                                                row["num_queens"],
                                                row["distance_km"],
                                                row["bonus_code"],
                                                row["final_cost"]
                                                ))



    def load_results(self): #main function
        rows = self.read_sales_file() #read CSV file
        if not rows: #provide an exit to prevent crashes, stopping if rows list is not found
            return
        rows = self.filter_sales(rows) #call the filter function to filter the list based on chosen combobox
        rows = self.sort_sales(rows) #call the sort function to sort the list based on chosen combobox
        self.display_sales(rows) #load list to treeview and displays data
        
        pass


def main():

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")

    BeeBayAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()