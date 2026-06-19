from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore

class HomeScreen(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)
        
        # create a label
        self.label_try = ttk.Label(self, text="Test!", font=("Archivo Black", 48), 
                            bootstyle="info") #inverse will make the background that colour rather than the text
        self.label_try.pack(pady=50) #15 minutes into video...

        # create a button
        self.button_try = ttk.Button(self, text="Submit", bootstyle="primary", 
                                    command=self.on_submit_click) #link to command!!!
        self.button_try.pack(pady=20)

        # create functions/methods for the buttons inside the class?
        def on_submit_click(self):
            print("Submit button clicked!")
