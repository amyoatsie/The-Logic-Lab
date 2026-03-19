total_cost = 0

print("")
print("Please enter one item at a time (Hot Dog, Burger, or Drink).\nEnter 'Done' when finished ordering.")
while True:
    item = str(input("What item would you like to purchase? ")).upper()

    if item == "DONE":
        break
    elif item == "HOT DOG":
        total_cost =+ 4.50
    elif item == "BURGER":
        total_cost =+ 6.00
    elif item == "DRINK":
        total_cost =+ 2.50
    else:
        print("Invalid Item Request.")

if total_cost > 20:
    discount = total_cost * 0.1
else:
    discount = 0

final_cost = total_cost - discount

print("Your final total is $" + str(final_cost))