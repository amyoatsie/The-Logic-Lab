# beebay_cli.py
import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent / "orders.csv" #saves csv withing module 1 folder
CSV_FIELDS = ["worker_bees", "queen_bees", "distance", "code", "cost"]

def ensure_csv_exists(): #a function rather than an if statement

    if CSV_PATH.exists() is True:
        return

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

def append_task(task_data): #!!!
    """Appends a single task dictionary to the CSV file."""
    ensure_csv_exists()
    # Open in 'a' (append) mode to add to the end of the file
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(task_data)
        #print("Saving to:", CSV_PATH.resolve()) - write where the file is saved

def check_queen_count(filename, num_queens):
    total_queens = 0

    #if file does not exist, allow save
    if not filename.exists():
        return True

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_queens += int(row["queen_bees"])

    # check limit
    if total_queens + num_queens > 10:
        return False
    else:
        return True


def save_tasks(tasks): #calls & runs the ensure_csv_exists function at the start
    ensure_csv_exists()

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for task in tasks:
            writer.writerow(
                {
                    "worker_bees": task["worker_bees"],
                    "queen_bees": task["queen_bees"],
                    "distance": task["distance"],
                    "code": task["code"],
                    "cost": task["cost"],
                }
            )



def calculate_post(distance_km):
    """ Determine postage cost based on delivery distance.

    TODO:
    Implement the distance rules:
        up to 50 km      -> $10
        up to 150 km     -> $20
        150 km or more   -> $30
    """

    postage_cost = 0

    #determines postage_cost using distance_km

    if distance_km < 10:
        postage_cost = 10
    elif distance_km < 150:
        postage_cost = 20
    else:
        postage_cost = 30

    return postage_cost


def main():

    # --- constants ---
    worker_price = 0.05
    queen_price = 15.00
    queen_surcharge_rate = 0.125

    print("BeeBay Order Cost Calculator")
    print("-----------------------------")

    # --- input --- (could define a function that's called for validation)
    num_workers = int(input("Number of worker bees: "))
    if num_workers < 0:
        print("Invalid input.")
        return
    num_queens = int(input("Number of queen bees: "))
    if num_queens < 0:
        print("Invalid input.")
        return
    distance_km = float(input("Delivery distance (km): "))
    if distance_km < 0:
        print("Invalid input.")
        return
    bonus_code = input("Bonus code (SALE / FREEPOST / HALFPOST or blank): ").upper()


    # --- processing ---

    #calculates worker_cost
    worker_cost = num_workers * worker_price

    #calculates queen_cost
    queen_cost = num_queens * queen_price

    #calculates bee_subtotal
    bee_subtotal = worker_cost + queen_cost

    #calculates queen surcharge amount if queen bees are ordered
    surcharge_amount = 0
    if num_queens > 0: #if there's a queen orders will update the surcharge
        surcharge_amount = bee_subtotal * queen_surcharge_rate

    # TODO: determine postage using calculate_post()
    postage_cost = calculate_post(distance_km) #check that this works

    #adjusts postage if bonus code is FREEPOST or HALFPOST
    if bonus_code.upper() == "FREEPOST":
        postage_cost = 0
    elif bonus_code.upper() == "HALFPOST":
        postage_cost = postage_cost / 2

    #calculates subtotal including bees, surcharge and postage
    subtotal = bee_subtotal + surcharge_amount + postage_cost

    #calculates discount amount if bonus code is SALE
    discount_amount = 0
    if bonus_code.upper() == "SALE":
        discount_amount = subtotal * 0.10

    #calculatess final total
    final_cost = subtotal - discount_amount


# --- csv update ---
    # Prepare data dictionary to match CSV_FIELDS
    new_task = {
        'worker_bees': num_workers,
        'queen_bees': num_queens,
        'distance': distance_km,
        'code': bonus_code,
        'cost': f"{final_cost:.2f}"
    }

    #queen validation
    can_save = True
    
    if num_queens > 10:
        can_save = False
    elif num_queens > 0:
        can_save = check_queen_count(CSV_PATH, num_queens)
    
    if can_save:
        append_task(new_task)
    else:
        print("Queen count exceeds daily limit.")
        return

    # --- output ---
    print()
    print("Order Summary")
    print("-----------------------------")

    print("Bee subtotal:   $", bee_subtotal)
    print("Surcharge:      $", round(surcharge_amount, 2))
    print("Postage:        $", postage_cost)
    print("Discount:       $", round(discount_amount, 2))

    print()
    print("Final total:    $", round(final_cost, 2))  #rounds to two decimals



if __name__ == "__main__":
    main()