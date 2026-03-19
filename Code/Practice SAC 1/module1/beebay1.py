# beebay_cli.py

def calculate_post(distance_km): #function to return the postage_cost based in the shipping distance
    postage_cost = 0

    #determine postage_cost using distance_km
    if distance_km < 10:
        postage_cost = 10
    elif distance_km < 150:
        postage_cost = 20
    else:
        postage_cost = 30

    return postage_cost

def main():

    # --- constants --- (ToDo: should likely make CAPS to indicate constant nature)
    worker_price = 0.05
    queen_price = 15.00
    queen_surcharge_rate = 0.125

    print("BeeBay Order Cost Calculator")
    print("-----------------------------")

    # --- inputs --- (ToDo: define a function that's called for validation)
    num_workers = int(input("Number of worker bees: ")) #ensure the input value for num_workers is an integer as it must be a whole number
    if num_workers < 0: #if input is invalid exit program
        return
    num_queens = int(input("Number of queen bees: ")) #ensure the input value for num_queens is an integer as it must be a whole number
    if num_queens < 0: #if input is invalid exit program
        return
    distance_km = float(input("Delivery distance (km): ")) #ensure the input value for num_workers is a float as it may be a decimal number
    if distance_km < 0: #if input is invalid exit program
        return
    bonus_code = input("Bonus code (SALE / FREEPOST / HALFPOST or blank): ").upper() 
    #reformats the users input into an all caps string to prevent logic errors associated with python not recognising the users input


    # --- processing ---
    #calculate worker_cost using the price constant and user input
    worker_cost = num_workers * worker_price
    #calculate queen_cost using the price constant and user input
    queen_cost = num_queens * queen_price
    #calculate bee_subtotal by adding together the previous costs
    bee_subtotal = worker_cost + queen_cost

    #calculate queen surcharge amount if queen bees are ordered
    surcharge_amount = 0
    if num_queens > 0: #if a queen  is ordered, will update the surcharge
        surcharge_amount = bee_subtotal * queen_surcharge_rate

    postage_cost = calculate_post(distance_km) #determines postage cost by calling the calculate_post function and passing in distance_km

    #adjust postage if bonus code is FREEPOST or HALFPOST
    if bonus_code == "FREEPOST":
        postage_cost = 0
    elif bonus_code == "HALFPOST":
        postage_cost = postage_cost / 2 #will make the postage "half" price to match the given code

    #calculate subtotal including bees, surcharge and postage
    subtotal = bee_subtotal + surcharge_amount + postage_cost

    #calculate discount amount if bonus code is SALE
    discount_amount = 0
    if bonus_code.upper() == "SALE":
        discount_amount = subtotal * 0.10 #calculate 10% discount

    #calculate final total
    final_cost = subtotal - discount_amount

    # --- output ---
    print()
    print("Order Summary")
    print("-----------------------------")

    #format all as 2 decimal places including trailing zeros
    print(f"Bee subtotal:   ${bee_subtotal:.2f}")
    print(f"Surcharge:      ${surcharge_amount:.2f}")
    print(f"Postage:        ${postage_cost:.2f}")
    print(f"Discount:       ${discount_amount:.2f}")
    print()
    print(f"Final total:    ${final_cost:.2f}")


if __name__ == "__main__":
    main()