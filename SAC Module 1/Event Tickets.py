

def main():
    while True: #Loop which continues until input is valid
        ticket_tier = str(input("Select a ticket tier (STANDARD, PREMIUM, VIP): ")).upper()     
        #Format the users input into an all caps string to prevent logic errors associated with python not recognising the users input
        if ticket_tier != "STANDARD" and ticket_tier != "PREMIUM" and ticket_tier != "VIP": #Validate that the chosen ticket is an actual option
            print("Invalid ticket tier selected. Please try again.")
        else:
            break

    while True: #Loop which continues until input is valid
        num_adults = int(input("Enter the number of adults: ")) #Ensure the input value for num_adults is an integer as it must be a whole number
            #ToDo: Add type and existence validation other than the above break for if the input is not an integer that doesn't immediately exit the program
        if num_adults < 0: #Range validation to ensure a positive integer as there cannot be a negative number of adults
            print("Invalid number entered. Please input a real positive integer.")
        else:
            break

    while True: #Loop which continues until input is valid
        num_children = int(input("Enter the number of children: ")) #Ensure the input value for num_children is an integer as it must be a whole number
            #ToDo: Add type and existence validation other than the above break for if the input is not an integer that doesn't immediately exit the program
        if num_children < 0: #Range validation to ensure a positive integer as there cannot be a negative number of children
            print("Invalid number entered. Please input a real positive integer.")
        else:
            break #If all inputs are valid continure the program and exit the while loop

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
    final_total = subtotal - discount #alculate final total 

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