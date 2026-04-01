from dataclasses import dataclass
from datetime import date

@dataclass
class Booking:
    DISCOUNT_RATE = 0.1 #set constants (in all caps for readability)

    #type hints, again for programmers readibility not program
    num_adults: int 
    num_children: int 
    ticket_tier: str
    event_date: str
    total_cost: float = 0 #give it a value if not passed in/pre-defined, but must list after non-default fields
    date_entered: str = None
    booking_id: str = None
        
    def calculate(self):
        # TODO: Implement the calculation logic from Module 1
        # create additional methods in this class for sub-calculations
        if self.ticket_tier == "Standard": 
            adult_price = 40.00
            child_price = 25.00
        elif self.ticket_tier == "Premium":
            adult_price = 70.00
            child_price = 45.00
        elif self.ticket_tier == "VIP":
            adult_price = 110.00
            child_price = 70.0
        else:
            raise ValueError("Invalid ticket tier")

        #Calculate the subtotal and number of tickets
        self.subtotal = (self.num_adults * adult_price) + (self.num_children * child_price) #ToD: Define a function to calculate cost
        total_tickets = self.num_adults + self.num_children

        self.discount = 0
        if total_tickets >= 5: #If the number of tickets is greater of equal to 5 apply a discount
            self.discount = self.subtotal * self.DISCOUNT_RATE #Calculate the discount as 10% of the current subtotal
        
        self.total_cost = self.subtotal - self.discount

        self.date_entered = date.today()

        return self.subtotal, self.discount, self.total_cost, self.ticket_tier, self.date_entered


    def to_csv_row(self):
        return{
            "booking_id": self.booking_id,
            "event_date": self.event_date,
            "ticket_tier": self.ticket_tier,
            "num_adults": self.num_adults,
            "num_children": self.num_children,
            "total_cost": self.total_cost,
            "date_entered": self.date_entered,
        }
        # TODO: return this booking as a list in the correct CSV field order
        # Order:
        # booking_id, event_date, ticket_tier, num_adults, num_children, total_cost, date_entered
        pass
