from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore CHANGE SCREEN NAME LMAO
from ttkbootstrap.scrolled import ScrolledText

class challengeScreenOne(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)
        
        #-------------------------------
        
        question_one = ["Australia", "Canada", "Germany", "Japan"] # change these lol
        question_two = ["Chloe", "Bob", "Patrick", "Jane"]
        question_three = ["Methods", "Literature", "Physics", "Software"]
        question_four = ["Cake", "Ice Cream", "Cookie", "Brownie"]

        #---------------------------------

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

        #comboboxes
        self.userAnswer1 = ttk.Combobox(self, style="H4.TCombobox", values=question_one, state=READONLY)
        self.userAnswer1.place(x=450, y=300, width=240, height=30)
        self.userAnswer2 = ttk.Combobox(self, style="H4.TCombobox", values=question_two, state=READONLY)
        self.userAnswer2.place(x=450, y=380, width=240, height=30)
        self.userAnswer3 = ttk.Combobox(self, style="H4.TCombobox", values=question_three, state=READONLY)
        self.userAnswer3.place(x=450, y=460, width=240, height=30)
        self.userAnswer4 = ttk.Combobox(self, style="H4.TCombobox", values=question_four, state=READONLY)
        self.userAnswer4.place(x=450, y=540, width=240, height=30)

        # create a button
        self.button_try = ttk.Button(self, text="Submit", style="H6.TButton", command=self.on_submit_click) #link to command!!!
        self.button_try.place(x=915, y=545, width=220, height=52) # allows exact placement

        # ---------------------------------------------------------------------!!!

        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=720, y=120, width=580, height=350)
        
        # Instantiate the tab frames inside the notebook container
        self.tab_metadata = metaDataTab(self.notebook)
        self.tab_noise = ttk.Frame(self.notebook, style='TFrame')
        self.tab_clone = ttk.Frame(self.notebook, style='TFrame')
        self.tab_error = ttk.Frame(self.notebook, style='TFrame')
        
        # Mount them as bottom tabs (to match the mockup)
        self.notebook.add(self.tab_metadata, text="Meta Data")
        self.notebook.add(self.tab_noise, text="Noise Analysis")
        self.notebook.add(self.tab_clone, text="Clone Detection")
        self.notebook.add(self.tab_error, text="Error Level")

#--------------------------------------------

        # create functions/methods for the buttons inside the class?
    def on_submit_click(self): # for testing!
        print("Submit button clicked!") #add navigation? or in different folder?

#--------------------------------------------

class metaDataTab(ttk.Frame): #will need to create for each tab
    """The workspace view that displays inside the 'Meta Data' notebook tab."""
    def __init__(self, parent):
        super().__init__(parent, style='TFrame')
        
        #lbl = ttk.Label(self, text="GPS Navigation Target Context", style='H3.TLabel')
        #lbl.pack(anchor=NW, padx=15, pady=15) (a title but not needed)
        
        self.console = ScrolledText(self, padding=5, autohide=True, )
        self.console.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.console.insert(END, "Awaiting submission execution data...") #change (this is the default display)