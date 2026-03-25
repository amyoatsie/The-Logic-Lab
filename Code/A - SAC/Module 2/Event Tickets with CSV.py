import csv
'''sources data from a CSV file as it is explicitly stated within the design brief and as alternate data types would not function 
as well (txt data is not structured enough and XML is over complicated for the programs given requirements)'''
from pathlib import Path
id_num = 0

CSV_PATH = Path(__file__).parent / "bookings.csv" #saves csv within module 2 folder
CSV_FIELDS = ["id_num", "ticket_tier", "num_adults", "num_children", "subtotal", "discount", "final_total"]

def ensure_csv_exists(): #a function to check whether the CSV currently exists and create it if it doesn't (needed to prevent duplicates or existence errors)
    if CSV_PATH.exists() is True:
        return

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

def append_task(task_data): #a function to append a single task dictionary to the CSV file to add the customers booking information
    ensure_csv_exists() #call the existence check function to ensure a CSV exists or create one if not before continuing
    # Open in 'a' (append) mode to add to the end of the CSV file
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(task_data)
        #print("Saving to:", CSV_PATH.resolve()) - write where the file is saved to locate potential errors

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_valid_integer(prompt): #a function to perform type, existence, and range validation on the users inputs to prevent errors
    while True:
        try:
            value = int(input(prompt))
            
            if value < 0:
                print("Invalid number entered. Please input a real positive integer.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def calculate_total(ticket_tier, num_adults, num_children):  #a function to perform all the calculations internally 
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
    subtotal = (num_adults * adult_price) + (num_children * child_price)
    total_tickets = num_adults + num_children

    discount = 0
    if total_tickets >= 5: #If the number of tickets is greater of equal to 5 apply a discount
        discount = subtotal * 0.10 #Calculate the discount as 10% of the current subtotal

    final_total = subtotal - discount

    return subtotal, discount, final_total

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_next_ID(filename): #a function to find the next ID that should be saved
    row_count = 0

    #if file does not exist, allow save
    if not filename.exists():
        next_id = 1
        next_id = str(next_id) #format next_id to 3 significant figures 
        return next_id #pass next_id out

    with open(filename, "r", newline="", encoding="utf-8") as f:
        with open(filename) as f:
            row_count = sum(1 for line in f) #increase the row count by one fore the no. of rows
            next_id = row_count
            next_id = str(next_id).zfill(3) #format next_id to 3 significant figures 
            return next_id #pass next_id out

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(): #a function to contain all the main programming and logic
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

    next_id = get_next_ID(CSV_PATH)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    # Prepare data dictionary to match CSV_FIELDS and update CSV
    new_task = {
        'id_num': get_next_ID(CSV_PATH), #call the get_next_ID function to pass in the calculated next ID
        'ticket_tier': ticket_tier,
        'num_adults': num_adults,
        'num_children': num_children,
        'subtotal': subtotal,
        'discount': discount,
        'final_total': final_total,
    }

    append_task(new_task) #call the append_task function to add the current task to the csv

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

    print("")
    print("Booking number " + (str(next_id)) + " was saved successfully.")

if __name__ == "__main__":
    main()