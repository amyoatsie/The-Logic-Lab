#vending machine

cost = float(input("How much does the item you want cost? $"))
paid = float(input("How much money are you inputting? $"))

if paid >= cost:
    change = paid - cost
    print("You will recieve $"+ str(change) +" change")
else:
    print("You have not inputted enough money.")