import csv
from tkinter import ttk, messagebox
from pathlib import Path

from models.task import Task

#repository aka a place to store stuff
#where all the logic happens, acts like a controller , where all the work happens

class TaskRepoCsv:
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