import csv
from models.order import Order
from pathlib import Path

class OrderRepo:
    def __init__(self, filename):
        self.filename = filename
        self.FIELDNAMES = ["sales_id","ticket_tier","num_adults","num_children","subtotal","discount","final_cost"] #fieldnames in accurate order

    def get_next_id(self): #.zfill(3)
        if not Path(self.filename).exists():
            self.create_file()
            return 1
        # 2. Open the CSV file for reading
        highest_id = 0
        with open(self.filename, mode="r", newline="", encoding="UTF-8") as file:
        # 3. Skip the header row
            reader = csv.DictReader(file)
        # 4. Find the highest existing sales_id
            for row in reader:
                if int(row["sales_id"]) > highest_id:
                    highest_id = int(row["sales_id"])
        # 5. Return the next ID 
        return highest_id + 1

    def get_valid_adults(self, num_adults): #a function to perform type, existence, and range validation on the users inputs to prevent errors
        #while True:
            try:
                value = int((num_adults))
            
                if value < 0:
                    #print("Invalid number entered. Please input a real positive integer.")
                    return False
                else:
                    return True
            
            except ValueError:
                #print("Invalid input. Please enter a valid integer.")
                return False

    def get_valid_children(self, num_children): #a function to perform type, existence, and range validation on the users inputs to prevent errors
        #while True:
            try:
                value = int((num_children))
            
                if value < 0:
                    return False
                else:
                    return True
            
            except ValueError:
                return False




    def create_file(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

    def save(self, order): #can keep the same, change the safe function in screen
        try:
            order.sales_id = str(self.get_next_id()).zfill(3)
            
            # 1. Open the CSV file in append mode
            with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            # 2. Write order.to_csv_row()
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writerow(order.to_dict())
            return True
        
        except Exception as e:
            print("SAVE ERROR:", e)
            return False #can get better error information, but this is enough for now
