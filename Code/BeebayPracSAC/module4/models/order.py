from dataclasses import dataclass

@dataclass
class Order:
    num_workers: int
    num_queens: int
    distance_km: float
    bonus_code: str
    final_cost: float = 0
    sales_id: int = None
    
    def calculate(self):
        worker_price = 0.05
        queen_price = 15.00
        queen_surcharge_rate = 0.125
        
        if self.distance_km < 10:
            postage_cost = 10
        elif self.distance_km < 150:
            postage_cost = 20
        else:
            postage_cost = 30
        
        #calculate worker_cost
        worker_cost = self.num_workers * worker_price
        #calculate queen_cost
        queen_cost = self.num_queens * queen_price
        #calculate bee_subtotal
        bee_subtotal = worker_cost + queen_cost
        #calculate queen surcharge amount if queen bees are ordered
        surcharge_amount = 0
        if self.num_queens > 0: #if there's a queen orders will update the surcharge
            surcharge_amount = bee_subtotal * queen_surcharge_rate

        #adjust postage if bonus code is FREEPOST or HALFPOST
        if self.bonus_code.upper() == "FREEPOST":
            postage_cost = 0
        elif self.bonus_code.upper() == "HALFPOST":
            postage_cost = postage_cost / 2

        #calculate subtotal including bees, surcharge and postage
        subtotal = bee_subtotal + surcharge_amount + postage_cost

        #calculate discount amount if bonus code is SALE
        discount_amount = 0
        if self.bonus_code.upper() == "SALE":
            discount_amount = subtotal * 0.10

        #calculate final total
        final_cost = subtotal - discount_amount
        
        
        self.final_cost = final_cost
    
    def to_csv_row(self):
        order = [self.sales_id, self.num_workers, self.num_queens, self.distance_km, self.bonus_code, self.final_cost]
        
        return order
    
        # TODO: return this order as a list in the correct CSV field order
        # Order:
        # sales_id, num_workers, num_queens, distance_km, bonus_code, final_cost


