import csv
from models.booking import Booking
from pathlib import Path

class BookingRepo:
    def __init__(self, filename):
        self.filename = filename
        self.fieldnames = ["booking_id","event_date","ticket_tier","num_adults","num_children","total_cost","date_entered"]


    def get_next_id(self):
        if not Path(self.filename).exists():
            self.create_file()
            return 1
        # 2. Open the CSV file for reading
        highest_id = 0
        with open(self.filename, mode="r", newline="", encoding="UTF-8") as file:
        # 3. Skip the header row
            reader = csv.DictReader(file)
        # 4. Find the highest existing booking_id
            for row in reader:
                if int(row["booking_id"]) > highest_id:
                    highest_id = int(row["booking_id"])
        # 5. Return the next ID 
        return highest_id + 1

    def get_valid_adults(self, num_adults): #a function to perform type, existence, and range validation on the users inputs to prevent errors
        #while True:
            try:
                value = int((num_adults))
            
                if value < 0:
                    return False
                else:
                    return True
            
            except ValueError:
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
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()


    def save(self, booking):
        try:
            booking.booking_id = str(self.get_next_id()).zfill(3) #makes id 3 figures
            
            # 1. Open the CSV file in append mode
            with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            # 2. Write booking.to_csv_row()
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writerow(booking.to_csv_row())
            return True
        
        except Exception as e:
            print("SAVE ERROR:", e)
            return False #can get better error information, but this is enough for now
