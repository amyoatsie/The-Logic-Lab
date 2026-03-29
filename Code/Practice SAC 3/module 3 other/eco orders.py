import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv


class EcoMarketAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="High Eco + Discount")
        self.sort_var = tk.StringVar(value="price")

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.eco_csv = BASE_DIR / "eco_orders.csv"

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        ttk.Label(self, text="EcoMarket Analytics", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 15)
        )

        ttk.Label(self, text="Filter:").grid(row=1, column=0, sticky="w")

        ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=[
                "High Eco + Discount",
                "High Eco No Discount",
                "Low Eco All"
            ]
        ).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Sort by:").grid(row=2, column=0, sticky="w")

        ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["price", "eco_rating"]
        ).grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Button(
            self,
            text="Load Analysis",
            command=self.load_results
        ).grid(row=2, column=2, padx=(10, 0))

        columns = (
            "order_id",
            "product_name",
            "category",
            "eco_rating",
            "price",
            "discount_applied"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew")

        headings = {
            "order_id": "Order ID",
            "product_name": "Product",
            "category": "Category",
            "eco_rating": "Eco Rating",
            "price": "Price",
            "discount_applied": "Discount"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

# ----------------------------

    def read_eco_orders_file(self): #function to read all of the CSV files and format them into a new list 'rows'
        rows = [] #create an empty list to append the relevant data which can be used for filtering/sorting
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        try:
            with open(self.eco_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["order_id"] = int(row["order_id"]) #convert order_id to an integer as it must be a whole number
                    row["eco_rating"] = int(row["eco_rating"]) #convert eco_rating tto an integer as it must be a whole number
                    row["price"] = float(row["price"]) #convert price to a float as it may be a decimal number
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.eco_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found

    def filter_eco_orders(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "High Eco + Discount" and row["eco_rating"] >= 4 and row["discount_applied"] == "Yes":
                #add each CSV row to the new filtered list which meets the selected filter criteria of High Eco + Discount
                filtered.append(row)
            elif filter_option == "High Eco No Discount" and row["eco_rating"] >= 4 and row["discount_applied"] == "No":
                #add each CSV row to the new filtered list which meets the selected filter criteria of High Eco No Discount
                filtered.append(row)
            elif filter_option == "Low Eco All" and row["eco_rating"] < 4:
                #add each CSV row to the new filtered list which meets the selected filter criteria of Low Eco All
                filtered.append(row)
            
        return filtered #exit function and pass out the new filtered list

    def sort_orders(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_var.get() #find the selected dropdown for sort by
        
        if sort_option == "price": #sort result list by price
            return sorted(rows, key=lambda x: (x["price"], x["eco_rating"])) #simplified version of list creation to reduce redundincy, with secondary sorting in case to prices match
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        elif sort_option == "eco_rating": #as there are currently only two sorting options else could be used, but elif prevents potential errors, with secondary sorting in case to ratings match
            return sorted(rows, key=lambda x: (x["eco_rating"], x["price"]))
        
        #ToDo: add a sorting function to sort by Order ID

    def display_orders(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["order_id"], 
                                                row["product_name"], 
                                                row["category"],
                                                row["eco_rating"],
                                                row["price"],
                                                row["discount_applied"]
                                                ))


# ----------------------------

    def load_results(self):
        rows = self.read_eco_orders_file() #read CSV file
        if not rows: #provide an exit to prevent crashes, stopping if rows list is not found
            return
        rows = self.filter_eco_orders(rows) #call the filter function to filter the list based on chosen combobox
        rows = self.sort_orders(rows) #call the sort function to sort the list based on chosen combobox
        self.display_orders(rows) #load list to treeview and displays data


def main():
    root = tk.Tk()
    root.title("EcoMarket Admin")
    root.geometry("850x450")

    EcoMarketAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()