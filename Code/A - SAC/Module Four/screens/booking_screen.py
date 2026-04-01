import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from models.booking import Booking
from repos.booking_repo import BookingRepo


class BookingScreen(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.repo = repo #passed from App
        self.order = None #to use in class methods

        self.fieldnames = ["booking_id","event_date","ticket_tier","num_adults","num_children","total_cost","date_entered"]

        self.grid(row=0, column=0, sticky="nsew")

        self.event_date_var = tk.StringVar()
        self.ticket_tier_var = tk.StringVar()
        self.num_adults_var = tk.StringVar()
        self.num_children_var = tk.StringVar()
        self.total_cost_var = tk.StringVar()

        self.date_entered_var = tk.StringVar()
        self.current_date = date.today()

        self.setup_grid()
        self.create_widgets()

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):
        ttk.Label(self, text="New Event Booking", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

    #TODO: Add input date validation for non-existent dates/type or previous dates
        ttk.Label(self, text="Event date:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(self, textvariable=self.event_date_var).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Ticket tier:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Combobox(
            self,
            textvariable=self.ticket_tier_var,
            state="readonly",
            values=["Standard", "Premium", "VIP"]
        ).grid(row=2, column=1, sticky="ew", pady=5)
        self.ticket_tier_var.set("Standard") #sets default

        ttk.Label(self, text="Number of adults:").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(self, textvariable=self.num_adults_var).grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Number of children:").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(self, textvariable=self.num_children_var).grid(row=4, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Date entered:").grid(row=5, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(self, textvariable=self.date_entered_var, state="readonly").grid(row=5, column=1, sticky="ew", pady=5)
        self.date_entered_var.set(date.today()) #insert the current date as default

        ttk.Label(self, text="Total cost:").grid(row=6, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(self, textvariable=self.total_cost_var, state="readonly").grid(row=6, column=1, sticky="ew", pady=5)

        ttk.Button(self, text="Calculate", command=self.calculate_total).grid(row=7, column=0, sticky="w", pady=(12, 0))
        ttk.Button(self, text="Save Booking", command=self.save_booking).grid(row=7, column=1, sticky="e", pady=(12, 0))

    def calculate_total(self):
        #validate inputs
        num_adults = int(self.num_adults_var.get())
        num_children = int(self.num_children_var.get())
        ticket_tier = self.ticket_tier_var.get()
        event_date = self.event_date_var.get()
        
        #main code
        #create order object from validated values
        self.order = Booking(num_adults, num_children, ticket_tier, event_date)
        #calculate values
        self.order.calculate()
        #update total on screen
        self.total_cost_var.set(f"${self.order.total_cost:.2f}")
        # TODO:
        # Validate all inputs
        # Reuse the logic from Module 1 to calculate the event booking total.
        # Standard: adult 40, child 25
        # Premium: adult 70, child 45
        # VIP: adult 110, child 70
        # Apply a 10% discount if total tickets is 5 or more.
        # Display the final total in total_cost_var.
        pass

    def save_booking(self):
        if self.order is None:
            messagebox.showwarning("Error", "Please calculate before saving.")
            return
        else:
            if (self.repo.get_valid_adults(self.num_adults_var.get())) and (self.repo.get_valid_children(self.num_children_var.get())):
                if(self.repo.save(self.order)):
                    messagebox.showinfo("Save success", "Order successfully saved")
                    #TODO: CLEAR FIELDS!
                else:
                        messagebox.showerror("Error", "Error saving Order")
            else:
                messagebox.showwarning("Error", "Invalid input. Please enter a valid positive integer.") #"No can do - too many Queens today" - mr pate
        # TODO:
        # 1. Get the next booking ID from the repository
        # 2. Create a Booking object
        # 3. Save the Booking object using the repository
        # 4. Display a confirmation message
        # 5. Clear the fields for a new entry !!!!!!!!!!AHHHHHHHHHHHHHHHHH

def main():
    root = tk.Tk()
    root.title("Concert Tickets - Module 4")
    root.geometry("620x320")

    BookingScreen(root)

    root.mainloop()


if __name__ == "__main__":
    main()