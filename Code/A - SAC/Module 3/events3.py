import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv


class ConcertTickets(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="All Tickets")
        self.sort_var = tk.StringVar(value="final_total")
        self.descending_var = tk.BooleanVar(value=False) #Add a descending option

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.bookings_csv = BASE_DIR / "events_bookings.csv"

    def setup_grid(self):

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):

        lbl_heading = ttk.Label(
            self,
            text="Concert Tickets",
            font=("Arial", 16, "bold")
        )
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        # ---------------- FILTER ----------------

        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=["All Tickets", "STANDARD", "PREMIUM", "VIP"]
        )
        cbo_filter.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Checkbutton(self, text="Descending", variable=self.descending_var)\
    .grid(row=1, column=2, padx=5) #Add a descending option

        # ---------------- SORT ----------------

        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["final_total", "num_tickets"]
        )
        cbo_sort.grid(row=2, column=1, sticky="ew", pady=5)

        btn_go = ttk.Button(
            self,
            text="Load Results",
            command=lambda: self.load_results()
        )
        btn_go.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=5)

        # ---------------- TABLE ----------------

        columns = (
            "id_num",
            "ticket_tier",
            "num_adults",
            "num_children",
            "subtotal",
            "discount",
            "final_total"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        headings = {
            "id_num": "Booking ID",
            "ticket_tier": "Tier",
            "num_adults": "Adults",
            "num_children": "Children",
            "subtotal": "Subtotal",
            "discount": "Discount",
            "final_total": "Final Total"
        }

        widths = {
            "id_num": 90,
            "ticket_tier": 110,
            "num_adults": 80,
            "num_children": 90,
            "subtotal": 110,
            "discount": 100,
            "final_total": 110
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)

# ----------------------------

    def read_bookings_file(self): #function to read all of the CSV files and format them into a new list 'rows'
        rows = [] #create an empty list to append the relevant data which can be used for filtering/sorting
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        try:
            with open(self.bookings_csv, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: #convert CSV data which may be used for filtering/sorting into numeric values
                    row["id_num"] = int(row["id_num"]) #convert id_num to an integer as it must be a whole number
                    row["final_total"] = float(row["final_total"]) #convert final_total to a float as it may be a decimal number
                    row["subtotal"] = float(row["subtotal"]) #convert subtotal to a float as it may be a decimal number
                    row["discount"] = float(row["discount"]) #convert discount to a float as it may be a decimal number
                    row["num_adults"] = int(row["num_adults"]) #convert num_adults to an integer as it must be a whole number
                    row["num_children"] = int(row["num_children"]) #convert num_children to an integer as it must be a whole number
                    rows.append(row) #add the formatted numeric fields and CSV rows to the empty list
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.bookings_csv}")
        return rows #exit function and return the empty list to prevent program from crashing if CSV file cannot be found

    def filter_bookings(self, rows): #function to filter rows based on the selected filter
        filtered = [] #create an empty list for the new filtered rows to be appended within
        #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        filter_option = self.filter_var.get() #passes in the selected combobox option
        for row in rows:
            if filter_option == "All Tickets":
                #add each CSV row to the new filtered list which meets the selected filter criteria of All
                filtered.append(row)
            elif filter_option == "STANDARD" and row["ticket_tier"] == "STANDARD":
                #add each CSV row to the new filtered list which meets the selected filter criteria of STANDARD
                filtered.append(row)
            elif filter_option == "PREMIUM" and row["ticket_tier"] == "PREMIUM":
                #add each CSV row to the new filtered list which meets the selected filter criteria of PREMIUM
                filtered.append(row)
            elif filter_option == "VIP" and row["ticket_tier"] == "VIP":
                #add each CSV row to the new filtered list which meets the selected filter criteria of VIP
                filtered.append(row)
        
        return filtered #exit function and pass out the new filtered list

    def sort_bookings(self, rows): #function to sort rows based on selected sort by
        sort_option = self.sort_var.get() #find the selected dropdown for sort by
        reverse_order = self.descending_var.get() #change the direction of sorting to descending if ticked
        
        if sort_option == "final_total": #sort result list by price
            return sorted(rows, key=lambda x: (x["final_total"], x["num_adults"] + x["num_children"]), reverse=reverse_order) #simplified version of list creation to reduce redundincy, with secondary sorting in case two final totals match
                            #sort by decending if selected
            #list is the chosen data structure to represent the array as it is the most effecient method within python 
        
        elif sort_option == "num_tickets": #as there are currently only two sorting options else could be used, but elif prevents potential errors, with secondary sorting in case two orders have the same # of tickets
            return sorted(rows, key=lambda x: (x["num_adults"] + x["num_children"], x["final_total"]), reverse=reverse_order)
        
        #ToDo: add a sorting function to sort by ID_Num

    def display_bookings(self, rows): #function to clear the treeview and display the new rows
        for i in self.tree.get_children(): #clear existing rows
            self.tree.delete(i)
        for row in rows:
            self.tree.insert("", "end", values=(row["id_num"], 
                                                row["ticket_tier"], 
                                                row["num_adults"],
                                                row["num_children"],
                                                f'${row["subtotal"]:.2f}',
                                                f'${row["discount"]:.2f}',
                                                f'${row["final_total"]:.2f}'
                                                )) #f"${row['subtotal']:.2f}"


# ----------------------------

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


# =====================================================

def main():

    root = tk.Tk()
    root.title("Concert Tickets")
    root.geometry("800x450")

    ConcertTickets(root)

    root.mainloop()


if __name__ == "__main__":
    main()