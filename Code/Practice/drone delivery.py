

distance_km = float(input("Distance (km): "))
weight_kg = float(input("Weight (kg): "))
express_delivery = str(input("Express Delivery? (Y/N): ")).upper()

if distance_km <= 5:
    base_cost = 6
elif distance_km <= 15:
    base_cost = 10
else:
    base_cost = 18

if weight_kg <= 2:
    weight_charge = 0
elif weight_kg <= 5:
    weight_charge = 4
else:
    weight_charge = 10

final_cost = base_cost + weight_charge

if express_delivery == "Y":
    final_cost = final_cost + 8

print("The final cost is $" + str(final_cost))