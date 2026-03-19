import csv
#from models.order import Order
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data" / "orders.csv" #saves csv
CSV_FIELDS = ["sales_id", "worker_bees", "queen_bees", "distance", "code", "cost"]


class OrderRepo:
    def __init__(self, filename):
        self.filename = filename
        
    def get_next_id(self):
        if self.CSV_PATH.exists() is not True: #If the file does not exist, create it, with headers and return 1
            with open(self.CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()
                return 1
        
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            #for row in reader:
            





        # TODO:
        # 1. If the file does not exist, create it, with headers and return 1
        # 2. Open the CSV file for reading
        # 3. Skip the header row
        # 4. Find the highest existing sales_id
        # 5. Return the next ID 


    def check_queen_count(self, num_queens):
        total_queens = 0
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_queens += int(row["queen_bees"])

        # check limit
        if total_queens + num_queens > 10: #ensure that num_queens (from new order) plus sum of queens in file < 11
            return False
        else:
            return True #return TRUE (if we can proceed with order) or FALSE (if too many queens)


    def save(self, order):
        if self.CSV_PATH.exists() is not True:
            return
        
        with open(self.CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_FIELDS)
            writer.writeheader()

            for task in order:
                writer.writerow(
                    {
                        "worker_bees": task["worker_bees"],
                        "queen_bees": task["queen_bees"],
                        "distance": task["distance"],
                        "code": task["code"],
                        "cost": task["cost"],
                    }
                )
        
        # TODO:
        # 1. Open the CSV file in append mode
        # 2. Write order.to_csv_row()
