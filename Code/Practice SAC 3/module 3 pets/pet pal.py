import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv

class PetPalAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="Priority Adoptions")
        self.sort_var = tk.StringVar(value="adoption_fee")

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.adoptions_csv = BASE_DIR / "adoptions.csv"

    def setup_grid(self):

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        ttk.Label(self, text="PetPal Adoption Manager", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 15)
        )

        ttk.Label(self, text="Filter:").grid(row=1, column=0, sticky="w")

        ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=["Priority Adoptions", "Standard Adoptions"]
        ).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Sort by:").grid(row=2, column=0, sticky="w")

        ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["adoption_fee", "distance_km"]
        ).grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Button(
            self,
            text="Load Results",
            command=self.load_results
        ).grid(row=2, column=2, padx=(10, 0))

        columns = (
            "adoption_id",
            "pet_type",
            "age_years",
            "adoption_fee",
            "distance_km",
            "priority_status"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        headings = {
            "adoption_id": "ID",
            "pet_type": "Pet Type",
            "age_years": "Age (Years)",
            "adoption_fee": "Fee ($)",
            "distance_km": "Distance (km)",
            "priority_status": "Priority"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns")

        self.tree.configure(yscrollcommand=scrollbar.set)

#-------------------------------------------

    def read_adoption_file(self): #function to read all of the CSV files and format them into a new list 'rows'
        rows = [] #create an empty list to append the relevant data which can be used for filtering/sorting
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        try:
            with open(self.adoptions_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["adoption_id"] = int(row["adoption_id"]) #convert adoption_id to an integer as it must be a whole number
                    row["adoption_fee"] = float(row["adoption_fee"]) #convert adoption_fee to a float as it may be a decimal number
                    row["distance_km"] = float(row["distance_km"]) #convert distance_km to a float as it may be a decimal number
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.sales_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found

    def filter_adoptions(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "Priority Adoptions" and row["priority_status"] == "Yes":
                #add each CSV row to the new filtered list which meets the selected filter criteria of at least 1 queen
                filtered.append(row)
            elif filter_option == "Standard Adoptions" and row["priority_status"] == "No":
                #add each CSV row to the new filtered list which meets the selected filter criteria of 0 queens
                filtered.append(row)
            
            #ToDo: add a filter 'All' to display all csv data
        return filtered #exit function and pass out the new filtered list

    def sort_sales(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_var.get() #find the selected dropdown for sort by
        
        if sort_option == "adoption_fee": #sort result list by adoption_fee
            return sorted(rows, key=lambda x: x["adoption_fee"]) #simplified version of list creation to reduce redundincy
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        else: #as there are currently only two sorting options, if it isn't one it will default to the other
            #ToDo: if more sorting options were added this must be changed to an elif statement
            return sorted(rows, key=lambda x: x["distance_km"])
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        #ToDo: add a sorting function to sort by Adoption ID

    def display_sales(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["adoption_id"], 
                                                row["pet_type"], 
                                                row["age_years"],
                                                row["adoption_fee"],
                                                row["distance_km"],
                                                row["priority_status"]
                                                ))



#-------------------------------------------

    def load_results(self):
        rows = self.read_adoption_file() #read CSV file
        if not rows: #provide an exit to prevent crashes, stopping if rows list is not found
            return
        rows = self.filter_adoptions(rows) #call the filter function to filter the list based on chosen combobox
        rows = self.sort_sales(rows) #call the sort function to sort the list based on chosen combobox
        self.display_sales(rows) #load list to treeview and displays data
    


def main():
    root = tk.Tk()
    root.title("PetPal Admin")
    root.geometry("800x420")

    PetPalAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()