from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore

class HomeScreen(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)
        
        self.title = ttk.Label(self, text="Metadata Analysis | Case 1", style="H1.TLabel", anchor='w') #inverse will make the background that colour rather than the text
        self.title.place(x=30, y=30) #15 minutes into video...

        # questions and numbers
        self.no1 = ttk.Label(self, text="1)", style="H2.TLabel", anchor='w')
        self.no1.place(x=30, y=280, width=40, height=70)
        self.question1 = ttk.Label(self, text="Question Number One", style="H3.TLabel", anchor='w')
        self.question1.place(x=70, y=280, width=640, height=70) #406-98 for adjustment !!!

        self.no2 = ttk.Label(self, text="2)", style="H2.TLabel", anchor='w')
        self.no2.place(x=30, y=360, width=40, height=70)
        self.question2 = ttk.Label(self, text="Question Number Two", style="H3.TLabel", anchor='w')
        self.question2.place(x=70, y=360, width=640, height=70) #+80 in y

        self.no3 = ttk.Label(self, text="3)", style="H2.TLabel", anchor='w')
        self.no3.place(x=30, y=440, width=40, height=70)
        self.question3 = ttk.Label(self, text="Question Number Three", style="H3.TLabel", anchor='w')
        self.question3.place(x=70, y=440, width=640, height=70)

        self.no4 = ttk.Label(self, text="4)", style="H2.TLabel", anchor='w')
        self.no4.place(x=30, y=520, width=40, height=70)
        self.question4 = ttk.Label(self, text="Question Number Four", style="H3.TLabel", anchor='w')
        self.question4.place(x=70, y=520, width=640, height=70) # might shrink the width?

        #dropdown
        self.userAnswer1 = ttk.Combobox(self, style="H4.TCombobox", state=READONLY)
        self.userAnswer1.place(x=450, y=300, width=240, height=30) #406-98 for adjustment !!!


        # create a button
        self.button_try = ttk.Button(self, text="Submit", style="H6.TButton", command=self.on_submit_click) #link to command!!!
        self.button_try.place(x=935, y=545, width=220, height=52) # allows exact placement

        # create functions/methods for the buttons inside the class?
    def on_submit_click(self): # for testing!
        print("Submit button clicked!")
