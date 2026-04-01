import tkinter as tk
from tkinter import ttk, messagebox
from models.order import Order
from repos.order_repo import OrderRepo

class OrderScreen(ttk.Frame):

    def __init__(self, parent, repo):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.repo = repo #passed from App
        self.order = None #to use in class methods

        self.FIELDNAMES = ["id_num", "ticket_tier", "num_adults", "num_children", "subtotal", "discount", "final_total"]

        self.grid(row=0, column=0, sticky="nsew")

        self.ticket_tier_var = tk.StringVar()
        self.num_adults_var = tk.StringVar()
        self.num_children_var = tk.StringVar()
        self.subtotal_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.final_cost_var = tk.StringVar()

        self.setup_grid()
        self.create_widgets()

    def setup_grid(self):

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):

        ttk.Label(
            self,
            text="Concert Ticket Booking System",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        ttk.Label(self, text="Ticket Tier:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Combobox(
            self,
            textvariable=self.ticket_tier_var,
            state="readonly",
            values=["STANDARD", "PREMIUM", "VIP"]
        ).grid(row=1, column=1, sticky="ew", pady=5)
        self.ticket_tier_var.set("STANDARD") #sets default

        ttk.Label(self, text="Number of Adult Tickets:").grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_adults_var).grid(
            row=2, column=1, sticky="ew", pady=5
        )

        ttk.Label(self, text="Number of Child Tickets:").grid(
            row=3, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_children_var).grid(
            row=3, column=1, sticky="ew", pady=5
        )

        ttk.Label(self, text="Final cost:").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.final_cost_var, state="readonly").grid(
            row=4, column=1, sticky="ew", pady=5
        )

        ttk.Button(self, text="Calculate", command=self.calculate).grid(
            row=5, column=0, sticky="w", pady=(12, 0)
        )
        ttk.Button(self, text="Save Order", command=self.save).grid(
            row=5, column=1, sticky="e", pady=(12, 0)
        )

    def calculate(self):
        #validate inputs
        num_adults = int(self.num_adults_var.get())
        num_children = int(self.num_children_var.get())
        ticket_tier = self.ticket_tier_var.get()
        
        #main code
        #create order object from validated values
        self.order = Order(num_adults, num_children, ticket_tier)
        #calculate values
        self.order.calculate()
        #update total on screen
        self.final_cost_var.set(f"${self.order.final_cost:.2f}")


    def save(self): #TODO!
        if self.order is None:
            messagebox.showwarning("Error", "Please calculate before saving.")
            return
        else:
            if (self.repo.get_valid_adults(self.num_adults_var.get())) and (self.repo.get_valid_children(self.num_children_var.get())):
                if(self.repo.save(self.order)):
                    messagebox.showinfo("Save success", "Order successfully saved")
                else:
                        messagebox.showerror("Error", "Error saving Order")
            else:
                messagebox.showwarning("Error", "Invalid input. Please enter a valid positive integer.") #"No can do - too many Queens today" - mr pate




def main():
    root = tk.Tk()
    root.title("Concert Tickets - Module 4")
    root.geometry("620x320")

    OrderScreen(root)

    root.mainloop()


if __name__ == "__main__":
    main()