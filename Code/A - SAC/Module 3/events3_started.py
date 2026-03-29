import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv
'''sources data from a CSV file as it is explicitly stated within the design brief and as alternate data types would not function 
as well (txt data is not structured enough and XML is over complicated for the programs given requirements) :)'''


class AdminSearchForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.event_date_var = tk.StringVar()
        self.sort_by_var = tk.StringVar(value="total_cost")
        self.descending_var = tk.BooleanVar(value=False) #Add a descending option

        BASE_DIR = Path(__file__).resolve().parent
        self.bookings_csv = BASE_DIR / "events_bookings.csv"

        self.setup_grid()
        self.create_widgets()

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def create_widgets(self):
        lbl_heading = ttk.Label(self, text="Admin Search", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        lbl_event_date = ttk.Label(self, text="Event date:")
        lbl_event_date.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        ent_event_date = ttk.Entry(self, textvariable=self.event_date_var)
        ent_event_date.grid(row=1, column=1, sticky="ew", pady=5)

        lbl_sort_by = ttk.Label(self, text="Sort by:")
        lbl_sort_by.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort_by = ttk.Combobox(
            self,
            textvariable=self.sort_by_var,
            state="readonly",
            values=["total_cost", "date_entered"]
        )
        cbo_sort_by.grid(row=2, column=1, sticky="ew", pady=5)

        btn_search = ttk.Button(self, text="Search", command=lambda: self.load_results())
        btn_search.grid(row=3, column=0, sticky="w", pady=(10, 10))

        ttk.Checkbutton(self, text="Descending", variable=self.descending_var)\
    .grid(row=3, column=1, padx=5) #Add a descending option

        columns = ("booking_id", "event_date", "ticket_tier", "num_adults", "num_children", "total_cost", "date_entered")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

        headings = {
            "booking_id": "Booking ID",
            "event_date": "Event Date",
            "ticket_tier": "Tier",
            "num_adults": "Adults",
            "num_children": "Children",
            "total_cost": "Total Cost",
            "date_entered": "Date Entered",
        }

        for column_name in columns:
            self.tree.heading(column_name, text=headings[column_name])
            self.tree.column(column_name, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

#---------------------------------------------------------

    def read_bookings_file(self): #function to read all of the CSV files and format them into a new list 'rows'
        rows = [] #create an empty list to append the relevant data which can be used for filtering/sorting
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        try:
            with open(self.bookings_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["booking_id"] = int(row["booking_id"]) #convert booking_id to an integer as it must be a whole number
                    row["total_cost"] = float(row["total_cost"]) #convert total_cost to a float as it may be a decimal number
                    row["num_adults"] = int(row["num_adults"]) #convert num_adults to an integer as it must be a whole number
                    row["num_children"] = int(row["num_children"]) #convert num_children to an integer as it must be a whole number
                    row["date_entered"] = str(row["date_entered"]) #convert date_entered to a string
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.bookings_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found
        
    

    def filter_bookings(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.event_date_var.get() #pass in the typed string
        for row in rows:
            if filter_option == row["date_entered"]: #if the inputted string matches the treeview value then add to the list and show
                filtered.append(row)
            elif filter_option == "": #if nothing is entered, show all
                filtered.append(row)
            
        #ToDo: Add external validation to provide user feedback for a string input such as 'Bob'
        
        return filtered #exit function and pass out the new filtered list



# ----------------

    def sort_bookings(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_by_var.get() #find the selected dropdown for sort by
        reverse_order = self.descending_var.get() #change the direction of sorting to descending if ticked
        
        if sort_option == "total_cost": #sort result list by price
            return sorted(rows, key=lambda x: (x["total_cost"], x["date_entered"]), reverse=reverse_order) #simplified version of list creation to reduce redundincy, with secondary sorting in case two final totals match
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        elif sort_option == "date_entered": #as there are currently only two sorting options else could be used, but elif prevents potential errors
            return sorted(rows, key=lambda x: (x["date_entered"], x["total_cost"]), reverse=reverse_order) #include secondary sorting in case two date_entered match
        
        #ToDo: add a sorting function to sort by booking_id

    def display_bookings(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["booking_id"], 
                                                row["event_date"], 
                                                row["ticket_tier"], 
                                                row["num_adults"],
                                                row["num_children"],
                                                f'${row["total_cost"]:.2f}',
                                                row["date_entered"]
                                                ))





#---------------------------------------------------------

    def load_results(self):
        rows = self.read_bookings_file() #read CSV file
        if not rows: #provide an exit to prevent crashes, stopping if rows list is not found
            return
        rows = self.filter_bookings(rows) #call the filter function to filter the list based on chosen combobox
        rows = self.sort_bookings(rows) #call the sort function to sort the list based on chosen combobox
        self.display_bookings(rows) #load list to treeview and displays data

        #except FileNotFoundError:
        #    messagebox.showerror("Error", "bookings.csv file not found.")
        #except Exception as e:
        #    messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    root.title("Event Ticketing Admin Search")
    root.geometry("900x450")

    AdminSearchForm(root)

    root.mainloop()

if __name__ == "__main__":
    main()
