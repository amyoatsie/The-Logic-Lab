import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent / "tickets.csv" #saves csv within module 1 folder
CSV_FIELDS = ["ticket_tier", "num_adults", "num_children", "final_total"]

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

def save_tasks(tasks): #calls & runs the ensure_csv_exists function at the start
    ensure_csv_exists()

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for task in tasks:
            writer.writerow(
                {
                    "ticket_tier": task["ticket_tier"],
                    "num_adults": task["num_adults"],
                    "num_children": task["num_children"],
                    "final_total": task["final_total"],
                }
            )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            
            if value < 0:
                print("Invalid number entered. Please input a real positive integer.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def calculate_total(ticket_tier, num_adults, num_children): #i was so damn close ima *!@ JOKING xoxo
    #Determine ticket prices based on ticket_tier
    if ticket_tier == "STANDARD": #
        adult_price = 40.00
        child_price = 25.00
    elif ticket_tier == "PREMIUM":
        adult_price = 70.00
        child_price = 45.00
    elif ticket_tier == "VIP":
        adult_price = 110.00
        child_price = 70.0

    #Calculate the subtotal and number of tickets
    subtotal = (num_adults * adult_price) + (num_children * child_price) #ToD: Define a function to calculate cost
    total_tickets = num_adults + num_children

    discount = 0
    if total_tickets >= 5: #If the number of tickets is greater of equal to 5 apply a discount
        discount = subtotal * 0.10 #Calculate the discount as 10% of the current subtotal

    final_total = subtotal - discount

    return subtotal, discount, final_total

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    while True: #Loop which continues until input is valid
        ticket_tier = str(input("Select a ticket tier (STANDARD, PREMIUM, VIP): ")).upper()     
        #Format the users input into an all caps string to prevent logic errors associated with python not recognising the users input
        if ticket_tier != "STANDARD" and ticket_tier != "PREMIUM" and ticket_tier != "VIP": #Validate that the chosen ticket is an actual option
            print("Invalid ticket tier selected. Please try again.")
        else:
            break

    num_adults = get_valid_integer("Enter the number of adults: ")
    num_children = get_valid_integer("Enter the number of children: ")

    subtotal, discount, final_total = calculate_total(ticket_tier, num_adults, num_children) 
    #Determine subtotal, discount, and final_total by calling the calculate_total function and passing in ticket_tier, num_adults, num_children

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    # Prepare data dictionary to match CSV_FIELDS and update CSV
    new_task = {
        'ticket_tier': ticket_tier,
        'num_adults': num_adults,
        'num_children': num_children,
        'final_total': final_total,
        #'cost': f"{final_cost:.2f}"
    }

    append_task(new_task)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~") #ToDo: Define a function 'print' for the output
    print("Order Summary")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Ticket Tier:     " + str(ticket_tier))
    print("Number of Adults: " + str(num_adults) + ", Number of Children: " + str(num_children))
        #format all as 2 decimal places including trailing zeros
    print(f"Subtotal:        ${subtotal:.2f}") 
    print(f"Discount:        ${discount:.2f}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Final total:     ${final_total:.2f}")

if __name__ == "__main__":
    main()