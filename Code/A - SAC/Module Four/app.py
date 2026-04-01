import tkinter as tk
from pathlib import Path
from repos.booking_repo import BookingRepo
from screens.booking_screen import BookingScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Event Booking - Module 4")
        self.root.geometry("700x420")

        base_dir = Path(__file__).resolve().parent
        data_file = base_dir / "data" / "bookings.csv"
        
        self.booking_repo = BookingRepo(data_file)
        BookingScreen(self.root, self.booking_repo)

    def run(self):
        self.root.mainloop()
