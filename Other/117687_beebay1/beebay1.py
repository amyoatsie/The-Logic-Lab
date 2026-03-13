# beebay_cli.py

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

    # --- input --- define a function that's called for validation
    num_workers = int(input("Number of worker bees: "))
    if num_workers < 0:
        return
    num_queens = int(input("Number of queen bees: "))
    if num_queens < 0:
        return
    distance_km = float(input("Delivery distance (km): "))
    if distance_km < 0:
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

    # --- output ---
    print()
    print("Order Summary")
    print("-----------------------------")

    print("Bee subtotal:   $", bee_subtotal)
    print("Surcharge:      $", round(surcharge_amount, 2))
    print("Postage:        $", postage_cost)
    print("Discount:       $", round(discount_amount, 2))

    print()
    print("Final total:    $", round(final_cost, 2))


if __name__ == "__main__":
    main()