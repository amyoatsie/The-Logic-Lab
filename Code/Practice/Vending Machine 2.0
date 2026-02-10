#vending machine
itemA = float(1.20)
itemB = float(0.60)
itemC = float(0.75)
paid = 0

chosen = str(input("Which item would you like? A, B, or C? ")).upper()

def coins(paid, price):
    moneyLeft = int(round((paid - price) * 100))
    coin2 = 0
    coin1 = 0
    coin50 = 0
    coin20 = 0
    coin10 = 0
    coin05 = 0
    
    while moneyLeft > 0:
        if paid < price:
            print("Insufficient payment.")
            break
        elif moneyLeft >= 200:
            moneyLeft -= 200
            coin2 = coin2 + 1
        elif moneyLeft >= 100:
            moneyLeft -= 100
            coin1 = coin1 + 1
        elif moneyLeft >= 50:
            moneyLeft -= 50
            coin50 = coin50 + 1
        elif moneyLeft >= 20:
            moneyLeft -= 20
            coin20 = coin20 + 1
        elif moneyLeft >= 10:
            moneyLeft -= 10
            coin10 = coin10 + 1
        elif moneyLeft >= 5:
            moneyLeft -= 5
            coin05 = coin05 + 1
        else:
            break
    print("Your change is $"+ str(paid - price) + " which will be paid by: \n$2 x " + str(coin2) + "\n$1 x " + str(coin1) + "\n$0.50 x " + str(coin50) +
          "\n$0.20 x " + str(coin20) + "\n$0.10 x " + str(coin10) + "\n$0.05 x " + str(coin05))

if chosen == "A":
    paid = float(input("Amount paid: $"))
    paidINT = int(round(paid * 100))
    if paidINT % 5 != 0:
        print("Error. Non-real input, please try again.")
    else:
        coins(paid, itemA)

elif chosen == "B":
    paid = float(input("Amount paid: $"))
    paidINT = int(round(paid * 100))
    if paidINT % 5 != 0:
        print("Error. Non-real input, please try again.")
    else:
        coins(paid, itemB)

elif chosen == "C":
    paid = float(input("Amount paid: $"))
    paidINT = int(round(paid * 100))
    if paidINT % 5 != 0:
        print("Error. Non-real input, please try again.")
    else:
        coins(paid, itemC)
