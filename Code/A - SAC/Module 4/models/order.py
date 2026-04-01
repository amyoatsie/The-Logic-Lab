from dataclasses import dataclass

@dataclass
class Order:
    DISCOUNT_RATE = 0.1 #set constants (in all caps for readability)
    
    num_adults: int #type hints, again for programmers readibility not program
    num_children: int
    ticket_tier: str
    subtotal: float = 0 #give it a value if not passed in/pre-defined, but must list after non-default fields
    discount: float = 0
    final_cost: float = 0
    sales_id: int = None
    

    def calculate(self): #
        #Determine ticket prices based on ticket_tier
        

        if self.ticket_tier == "STANDARD": 
            adult_price = 40.00
            child_price = 25.00
        elif self.ticket_tier == "PREMIUM":
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
        
        self.final_cost = self.subtotal - self.discount
        return self.subtotal, self.discount, self.final_cost, self.discount, self.ticket_tier

    def to_dict(self):
        #this is better called to_dict - sorry!! -mr pate
        return {
            "sales_id": self.sales_id,
            "num_adults": self.num_adults,
            "num_children": self.num_children,
            "subtotal": self.subtotal,
            "discount": self.discount,
            "ticket_tier": self.ticket_tier,
            "final_cost": self.final_cost,
        }


