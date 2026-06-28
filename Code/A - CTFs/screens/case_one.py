from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM - hasn't really been used, remove?
import ttkbootstrap as ttk # type: ignore
#from ttkbootstrap.scrolled import ScrolledText - no longer used
from PIL import Image, ImageTk
from pathlib import Path

class challengeScreenOne(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)

        SCREENS_DIR = Path(__file__).resolve().parent
        DATA_DIR = SCREENS_DIR.parent / "data"

        image_names = ["errorLevel", "luminanceGradient", "differenceAnalysis", "imageInfo"]
        
        # Initialize an empty dictionary
        self.icons = {}

        for name in image_names:
            img_path = DATA_DIR / f"{name}.png"
            raw_img = Image.open(img_path)
            raw_img.thumbnail((520, 315))
            self.icons[name] = ImageTk.PhotoImage(raw_img) # Save it into the dictionary using its name as the key

        #-------------------------------
        
        question_one = ["Methods", "Literature", "Physics", "Software"] # change these lol
        question_two = ["Chloe", "Bob", "Patrick", "Jane"]
        question_three = ["Red & Green", "Blue & Yellow", "Orange & Green", "Pink & Blue"] # research how difference analysis changes colours? 
        question_four = ["Cake", "Ice Cream", "Cookie", "Brownie"]

        #---------------------------------

        self.title = ttk.Label(self, text="Metadata Analysis | Case 1", style="H1.TLabel", anchor='w') # change the heading to forensics cause more so image forensics than metadata now?
        self.title.place(x=30, y=30)

        self.explain = ttk.Label(self, text="The first challenges revolves around the idea of forensic analysis. This ???", style="H4.TLabel", anchor='w')
        self.explain.place(x=30, y=100) #might move questions up and extend notebook height for text? ADD EXPLAIN

        # questions and numbers
        self.no1 = ttk.Label(self, text="1)", style="H2.TLabel", anchor='w')
        self.no1.place(x=30, y=280, width=40, height=70)
        self.question1 = ttk.Label(self, text="Question Number One", style="H3.TLabel", anchor='w')
        self.question1.place(x=70, y=280, width=640, height=70) #406-98 for adjustment !!!

        self.no2 = ttk.Label(self, text="2)", style="H2.TLabel", anchor='w')
        self.no2.place(x=30, y=360, width=40, height=70)
        self.question2 = ttk.Label(self, text="What section of the screen has inconsistencies?", style="H3.TLabel", anchor='w')
        self.question2.place(x=70, y=360, width=640, height=70) #+80 in y

        self.no3 = ttk.Label(self, text="3)", style="H2.TLabel", anchor='w')
        self.no3.place(x=30, y=440, width=40, height=70)
        self.question3 = ttk.Label(self, text="???", style="H3.TLabel", anchor='w')
        self.question3.place(x=70, y=440, width=640, height=70)

        self.no4 = ttk.Label(self, text="4)", style="H2.TLabel", anchor='w')
        self.no4.place(x=30, y=520, width=40, height=70)
        self.question4 = ttk.Label(self, text="What are the colours of the added objects?", style="H3.TLabel", anchor='w')
        self.question4.place(x=70, y=520, width=640, height=70)

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
        self.button_try.place(x=910, y=545, width=220, height=52) # might inverse colouring? (to match the primary and highlight as info), AND centre x once notebook is finalised

        # ---------------------------------------------------------------------!!!

        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=720, y=100, width=580, height=390)
        

        self.tab_luminance = ImageTab(self.notebook, self.icons["luminanceGradient"],
        "Figure 1.1: Areas with inconsistent noise patterns.")

        self.tab_error = ImageTab(self.notebook, self.icons["errorLevel"],
        "Figure 1.2: Error level analysis output.")

        self.tab_difference = ImageTab(self.notebook, self.icons["differenceAnalysis"],
        "Figure 1.3: Visualizing structural file discrepancies.")

        self.tab_info = ImageTab(self.notebook, self.icons["imageInfo"],
        "Figure 1.4: Additional background information.")

        self.notebook.add(self.tab_luminance, text=" Luminance Gradient ")
        self.notebook.add(self.tab_error, text=" Error Level Analysis ")
        self.notebook.add(self.tab_difference, text=" Difference Analysis ")
        self.notebook.add(self.tab_info, text="  Image Info  ") # spaces act as internal button padding

#--------------------------------------------

        # create functions/methods for the buttons inside the class?
    def on_submit_click(self): # for testing!
        print("Submit button clicked!") #add navigation? or in different folder?
    

#--------------------------------------------

class ImageTab(ttk.Frame):
    def __init__(self, parent, image_obj, caption):
        super().__init__(parent, style='TFrame')
        self.img = image_obj

        self.caption_label = ttk.Label(
            self,
            text=caption,
            style='H4.TLabel',
            wraplength=520,
            anchor='center')
        self.caption_label.pack(padx=20, pady=(0, 0))

        self.image_label = ttk.Label(
            self,
            image=self.img)
        self.image_label.pack(pady=(5, 10))

#--------------------------------------------