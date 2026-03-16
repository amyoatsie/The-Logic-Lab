import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv

class GameStoreAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="Premium Orders")
        self.sort_var = tk.StringVar(value="price")

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.orders_csv = BASE_DIR / "game_orders.csv"

    def setup_grid(self):

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        lbl_heading = ttk.Label(self, text="GameStore Order Manager", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=["Premium Orders", "Budget Orders"]
        )
        cbo_filter.grid(row=1, column=1, sticky="ew", pady=5)

        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["price", "download_size_gb"]
        )
        cbo_sort.grid(row=2, column=1, sticky="ew", pady=5)

        btn_go = ttk.Button(self, text="Load Results", command=lambda: self.load_results())
        btn_go.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=5)

        columns = (
            "order_id",
            "customer_name",
            "game_title",
            "price",
            "download_size_gb",
            "discount_code"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        headings = {
            "order_id": "Order ID",
            "customer_name": "Customer",
            "game_title": "Game Title",
            "price": "Price ($)",
            "download_size_gb": "Download Size (GB)",
            "discount_code": "Discount Code"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)

# -------------------------------------------
    def read_orders_file(self):
        rows = []        
        
        try:
            with open(self.orders_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["order_id"] = int(row["order_id"]) #convert order_id to an integer as it must be a whole number
                    row["price"] = float(row["price"]) #convert price to a float as it may be a decimal number 
                    row["download_size_gb"] = int(row["download_size_gb"]) #convert download_size_gb to an integer as in the context it must be a whole number                    
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.orders_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found

    def filter_orders(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "Budget Orders" and row["price"] < 60:
                #add each CSV row to the new filtered list which meets the selected filter criteria of a cost of less than $60
                filtered.append(row)
            elif filter_option == "Premium Orders" and row["price"] >= 60:
                #add each CSV row to the new filtered list which meets the selected filter criteria of a cost of $60 or more
                filtered.append(row)
            
            #ToDo: add a filter 'All' to display all csv data
        return filtered #exit function and pass out the new filtered list

    def sort_orders(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_var.get() #find the selected dropdown for sort by
        
        if sort_option == "price": #sort result list by final cost
            return sorted(rows, key=lambda x: x["price"]) #simplified version of list creation to reduce redundincy
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        else: #as there are currently only two sorting options, if it isn't one it will default to the other
            #ToDo: if more sorting options were added this must be changed to an elif statement
            return sorted(rows, key=lambda x: x["download_size_gb"])
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        #ToDo: add a sorting function to sort by Sale ID

    def display_sales(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["order_id"], 
                                                row["customer_name"], 
                                                row["game_title"],
                                                row["price"],
                                                row["download_size_gb"],
                                                row["discount_code"]
                                                ))

    def load_results(self): #main function
        rows = self.read_orders_file() #read CSV file
        if not rows: #provide an exit to prevent crashes, stopping if rows list is not found
            return
        rows = self.filter_orders(rows) #call the filter function to filter the list based on chosen combobox
        rows = self.sort_orders(rows) #call the sort function to sort the list based on chosen combobox
        self.display_sales(rows) #load list to treeview and displays data
        
        pass


def main():

    root = tk.Tk()
    root.title("GameStore Order Manager")
    root.geometry("800x420")

    GameStoreAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()