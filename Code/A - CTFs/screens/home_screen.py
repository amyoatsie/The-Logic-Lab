from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore 
from pathlib import Path
from models.challenge_logic import ChallengeEvaluator
#from screens.custom_popup import ResultPopup

READONLY = "readonly"

class homeScreen(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent, app):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)
        self.app = app

        SCREENS_DIR = Path(__file__).resolve().parent
        DATA_DIR = SCREENS_DIR.parent / "data"
        csv_path = DATA_DIR / "progress.csv"
        self.evaluator = ChallengeEvaluator(csv_path) # pass csv path into challenge evaluator

        #-------------------------------
        
        case_data = [ #centralised list of dictionaries to allow easier editing
            {"title": "Case 01 | Metadata Analysis",
                "text": "Understading hidden information in files"},
            {"title": "Case 02 | Digital Forensic Analysis",
                "text": "Analysing evidence and reconstructing events"},
            {"title": "Case 03 | Social Engineering",
                "text": "Phishing, impersonation, & manipulation tactics"},
            {"title": "Case 04 | Cryptography",
                "text": "Encryption, hashing, & secure communication"}]

        #---------------------------------

        self.title = ttk.Label(self, text="Welcome Back, _____", style="H1.TLabel", anchor='w') # add username input!!!
        self.title.place(x=30, y=40)

        #???

        '''self.no1 = ttk.Label(self, text="Questions", style="H2-2.TLabel", anchor='w')
        self.no1.place(x=30, y=275, width=150, height=70)'''

        # questions and numbers
        self.no1 = ttk.Label(self, text="1)", style="H2.TLabel", anchor='w') #add symbols???
        self.no1.place(x=30, y=330, width=40, height=70)
        self.case1 = ttk.Label(self, text=case_data[0]["title"], style="HS2.TLabel", anchor='nw', #add upper padding
                                justify="left", wraplength=450)
        self.case1.place(x=70, y=330, width=640, height=70)
        self.description1 = ttk.Label(self, text=case_data[0]["text"], style="HS4.TLabel", anchor='w')
        self.description1.place(x=70, y=365)

        self.no2 = ttk.Label(self, text="2)", style="H2.TLabel", anchor='w')
        self.no2.place(x=30, y=410, width=40, height=70)
        self.case2 = ttk.Label(self, text=case_data[1]["title"], style="HS2.TLabel", anchor='nw', #add upper padding
                                justify="left", wraplength=450)
        self.case2.place(x=70, y=410, width=640, height=70)
        self.description2 = ttk.Label(self, text=case_data[1]["text"], style="HS4.TLabel", anchor='w')
        self.description2.place(x=70, y=445)

        self.no3 = ttk.Label(self, text="3)", style="H2.TLabel", anchor='w')
        self.no3.place(x=30, y=490, width=40, height=70)
        self.case3 = ttk.Label(self, text=case_data[2]["title"], style="HS2.TLabel", anchor='nw', #add upper padding
                                justify="left", wraplength=450)
        self.case3.place(x=70, y=490, width=640, height=70)
        self.description3 = ttk.Label(self, text=case_data[2]["text"], style="HS4.TLabel", anchor='w')
        self.description3.place(x=70, y=525)

        self.no4 = ttk.Label(self, text="4)", style="H2.TLabel", anchor='w')
        self.no4.place(x=30, y=570, width=40, height=70)
        self.case4 = ttk.Label(self, text=case_data[3]["title"], style="HS2.TLabel", anchor='nw', #add upper padding
                                justify="left", wraplength=450)
        self.case4.place(x=70, y=570, width=640, height=70)
        self.description4 = ttk.Label(self, text=case_data[3]["text"], style="HS4.TLabel", anchor='w')
        self.description4.place(x=70, y=605)

        # create a button
        self.button_continue = ttk.Button(self, text="Start Case 1", style="H6.TButton", command=self.app.show_case_one)
        self.button_continue.place(x=910, y=590, width=220, height=52) # might inverse colouring? (to match the primary and highlight as info), AND centre x once notebook is finalised

        # ---------------------------------------------------------------------!!!
