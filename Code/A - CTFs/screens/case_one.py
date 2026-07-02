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
        question_two = ["Top", "Middle", "Bottom"]
        question_three = ["Cake", "Ice Cream", "Cookie", "Brownie"]
        question_four = ["Red & Green", "Blue & Yellow", "Orange & Green", "Pink & Blue"]

        #---------------------------------

        self.title = ttk.Label(self, text="Metadata Analysis | Case 1", style="H1.TLabel", anchor='w') # change the heading to forensics cause more so image forensics than metadata now?
        self.title.place(x=30, y=40)

        self.explain = ttk.Label(self, text="""The first challenges revolves around the idea of forensic analysis. This challenge features four screens which can be viewed by clicking the labels on the right, and each question will correspond primarily to the figure with the same number.\n~
Figure 1.1 ~ Helps identify altered objects by showing inconsistent noise patterns.
Figure 1.2 ~ Helps expose pasted objects as they glow brighter than the original image.
Figure 1.3 ~ Helps highlight altered objects by visualizing hidden file changes.
Figure 1.4 ~ Additional background information.""", 
                                style="H4.TLabel", anchor='w', justify="left", wraplength=680)
        self.explain.place(x=30, y=120)
        #question title
        self.no1 = ttk.Label(self, text="Questions", style="H2-2.TLabel", anchor='w')
        self.no1.place(x=30, y=275, width=150, height=70)

        # questions and numbers
        self.no1 = ttk.Label(self, text="1)", style="H2.TLabel", anchor='w')
        self.no1.place(x=30, y=330, width=40, height=70)
        self.question1 = ttk.Label(self, text="Question Number One with a lot of extra text for testing sake. La di da. e.t.c.", style="H3.TLabel", anchor='w', 
                                justify="left", wraplength=450)
        self.question1.place(x=70, y=330, width=640, height=70) #406-98 for adjustment !!!

        self.no2 = ttk.Label(self, text="2)", style="H2.TLabel", anchor='w')
        self.no2.place(x=30, y=410, width=40, height=70)
        self.question2 = ttk.Label(self, text="What section of the screen shows compression inconsistencies?", style="H3.TLabel", anchor='w',
                                justify="left", wraplength=450)
        self.question2.place(x=70, y=410, width=640, height=70) #+80 in y

        self.no3 = ttk.Label(self, text="3)", style="H2.TLabel", anchor='w')
        self.no3.place(x=30, y=490, width=40, height=70)
        self.question3 = ttk.Label(self, text="???", style="H3.TLabel", anchor='w',
                                justify="left", wraplength=450)
        self.question3.place(x=70, y=490, width=640, height=70)

        self.no4 = ttk.Label(self, text="4)", style="H2.TLabel", anchor='w')
        self.no4.place(x=30, y=570, width=40, height=70)
        self.question4 = ttk.Label(self, text="What were the original colours of the objects which were added in the altered image?", style="H3.TLabel", anchor='w',
                                justify="left", wraplength=450)
        self.question4.place(x=70, y=570, width=640, height=70)

        #comboboxes
        self.userAnswer1 = ttk.Combobox(self, style="H4.TCombobox", values=question_one, state=READONLY)
        self.userAnswer1.place(x=530, y=350, width=160, height=30)
        self.userAnswer2 = ttk.Combobox(self, style="H4.TCombobox", values=question_two, state=READONLY)
        self.userAnswer2.place(x=530, y=430, width=160, height=30)
        self.userAnswer3 = ttk.Combobox(self, style="H4.TCombobox", values=question_three, state=READONLY)
        self.userAnswer3.place(x=530, y=510, width=160, height=30)
        self.userAnswer4 = ttk.Combobox(self, style="H4.TCombobox", values=question_four, state=READONLY)
        self.userAnswer4.place(x=530, y=590, width=160, height=30)

        # create a button
        self.button_try = ttk.Button(self, text="Submit", style="H6.TButton", command=self.on_submit_click) #link to command!!!
        self.button_try.place(x=910, y=590, width=220, height=52) # might inverse colouring? (to match the primary and highlight as info), AND centre x once notebook is finalised

        # ---------------------------------------------------------------------!!!

        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=720, y=120, width=580, height=410)
        

        self.tab_luminance = ImageTab(self.notebook, self.icons["luminanceGradient"],
        "Luminance Gradient | shows variations in brightness (luminance) across an image to expose physical inconsistencies")

        self.tab_error = ImageTab(self.notebook, self.icons["errorLevel"],
        "Error Level Analysis (ELA) | highlights differences in image quality from saving a JPEG (compressing an image)")

        self.tab_difference = ImageTab(self.notebook, self.icons["differenceAnalysis"],
        "Difference Analysis | compares a photo against its own hidden 'original thumbnail' to reveal hidden changes")

        self.tab_info = ImageTab(self.notebook, self.icons["imageInfo"],
        "\nImage Info | ???")

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