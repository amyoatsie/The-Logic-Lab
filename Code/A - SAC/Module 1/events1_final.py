"""
events1.py
Module 1 exemplar: Event ticket calculation (no GUI)
"""

# Price table for each ticket tier
PRICES = {
    "Standard": {"adult": 40.00, "child": 25.00},
    "Premium": {"adult": 70.00, "child": 45.00},
    "VIP": {"adult": 110.00, "child": 70.00}
}


def get_ticket_tier():
    # Ask until a valid tier is entered
    while True:
        tier = input("Enter ticket tier (Standard, Premium, VIP): ").strip()
        if tier in PRICES:
            return tier
        print("Invalid tier. Please enter Standard, Premium or VIP.")


def get_whole_number(prompt):
    # Read a whole number that is 0 or greater
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number >= 0:
                return number
            print("Please enter 0 or a positive whole number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def calculate_booking(ticket_tier, num_adults, num_children):
    # Select prices for the chosen tier
    adult_price = PRICES[ticket_tier]["adult"]
    child_price = PRICES[ticket_tier]["child"]

    # Calculate subtotal and discount
    subtotal = (num_adults * adult_price) + (num_children * child_price)
    total_tickets = num_adults + num_children

    discount = 0.00
    if total_tickets >= 5:
        discount = subtotal * 0.10

    final_total = subtotal - discount

    return {
        "ticket_tier": ticket_tier,
        "num_adults": num_adults,
        "num_children": num_children,
        "subtotal": subtotal,
        "discount": discount,
        "final_total": final_total
    }


def display_booking(booking):
    # Output the booking details clearly
    print("\n--- Event Ticket Booking Summary ---")
    print(f"Ticket tier: {booking['ticket_tier']}")
    print(f"Adults: {booking['num_adults']}")
    print(f"Children: {booking['num_children']}")
    print(f"Subtotal: ${booking['subtotal']:.2f}")
    print(f"Discount: ${booking['discount']:.2f}")
    print(f"Final total: ${booking['final_total']:.2f}")


# Main program
print("Event Ticket Booking Calculator")
print("-------------------------------")

ticket_tier = get_ticket_tier()
num_adults = get_whole_number("Enter number of adult tickets: ")
num_children = get_whole_number("Enter number of child tickets: ")

# Basic existence check for the booking
if num_adults + num_children == 0:
    print("At least one ticket must be booked.")
else:
    booking = calculate_booking(ticket_tier, num_adults, num_children)
    display_booking(booking)
