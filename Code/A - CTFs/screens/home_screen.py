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

    #---------------------------------

        # Parse (NOT PASS LMAO) highest successfully completed case number from csv file
        self.completed_cases = self.get_completed_cases_from_csv(csv_path)
        self.total_challenges = 4

        self.completed_count = len(self.completed_cases)
        
        # Determine current target case (with an index)
        if not self.completed_cases:
            self.current_case_id = 1
        else:
            self.current_case_id = min(max(self.completed_cases) + 1, self.total_challenges)

        self.current_case_title = f"Case {self.current_case_id:02d}"
        self.current_case_sub_progress = 0 
        self.max_sub_challenges = 4

    #-------------------------------
        
        self.case_definitions = [ #centralised list of dictionaries to allow easier editing
            {"id": 1, "title": "Case 01 | Metadata Analysis",
                "description": "Understading hidden information in files", "command": self.app.show_case_one},
            {"id": 2, "title": "Case 02 | Digital Forensic Analysis",
                "description": "Analysing evidence and reconstructing events"}, #add command when screen is created
            {"id": 3, "title": "Case 03 | Social Engineering",
                "description": "Phishing, impersonation, & manipulation tactics"},
            {"id": 4, "title": "Case 04 | Cryptography",
                "description": "Encryption, hashing, & secure communication"}]
        
        self.create_widgets()


    def get_completed_cases_from_csv(self, path):
        """Reads the progress file to track successful cases."""
        completed = set()
        if not path.exists():
            return completed
        try:
            with open(path, "r") as f:
                lines = f.readlines()
                for line in lines[1:]:
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        case_str = parts[1]    # e.g., "Case 1"
                        result_str = parts[4]  # e.g., "Pass"
                        if result_str.strip().lower() == "pass":
                            num = int(''.join(filter(str.isdigit, case_str)))
                            completed.add(num)
        except Exception:
            pass
        return completed

    #---------------------------------

    def create_widgets(self):
        self.title = ttk.Label(self, text="Welcome Back, _____", style="H1.TLabel", anchor='w') # add username input!!!
        self.title.place(x=30, y=40)

        progress = ttk.Frame(self, style="Card.TFrame", padding=15)
        progress.place(x=30, y=110, width=650, height=120)

        ttk.Label(progress, text="OVERALL PROGRESS", style="HS5.TLabel").pack(anchor="w")

        # Dynamically linked to total challenges completed
        self.progress = ttk.Progressbar(progress, maximum=self.total_challenges, 
            value=self.completed_count, style="Logic.Horizontal.TProgressbar")
        self.progress.pack(fill=X, pady=12)

        ttk.Label(  progress, 
            text=f"{self.completed_count} / {self.total_challenges} Challenges Completed", 
            style="H5.TLabel"
        ).pack(anchor="e")

        # Right Panels
        self.create_continue_card()
        self.create_profile_card()

        # Case Cards Setup Loop
        start_y = 260
        for config in self.case_definitions:
            if config["id"] in self.completed_cases:
                status = "Completed"
            elif config["id"] == self.current_case_id:
                status = "Unlocked"
            else:
                status = "Locked"

            card = CaseCard(self, config, status)
            card.place(x=30, y=start_y, width=650, height=80)
            start_y += 90

    def create_continue_card(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        frame.place(x=730, y=40, width=580, height=170)

        ttk.Label(frame, text="CONTINUE LAST CHALLENGE", style="HS5.TLabel").pack(anchor="w")
        ttk.Label(frame, text=self.current_case_title, style="H3.TLabel").pack(anchor="w", pady=(10,0))

        # Dynamic subtask progress matching active workspace step
        ttk.Progressbar(
            frame, 
            maximum=self.max_sub_challenges, 
            value=self.current_case_sub_progress, 
            style="Logic.Horizontal.TProgressbar"
        ).pack(fill=X, pady=10)

        active_idx = self.current_case_id - 1
        active_command = self.case_definitions[active_idx].get("command", None)
        btn_state = NORMAL if active_command else DISABLED

        ttk.Button(frame, text="Continue", style="H6.TButton", 
                command=active_command, state=btn_state).pack(anchor="w")

    def create_profile_card(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        frame.place(x=730, y=240, width=580, height=140)

        ttk.Label(frame, text="PROFILE SETTINGS", style="HS5.TLabel").pack(anchor="w")

        button_frame = ttk.Frame(frame, style="Card.TFrame")
        button_frame.pack(fill=X, pady=20)

        ttk.Button(button_frame, text="Sign Out", style="H6.TButton").pack(side=LEFT)
        ttk.Button(button_frame, text="Reset Progress", style="H6.TButton").pack(side=RIGHT)

class CaseCard(ttk.Frame):
    def __init__(self, parent, data, status):
        # Added explicit Card style here to fix the missing background color
        super().__init__(parent, padding=10, style="Card.TFrame")

        ttk.Label(self, text=data["title"], style="HS2.TLabel", wraplength=380).place(x=15, y=5)
        ttk.Label(self, text=data["description"], style="HS4.TLabel", wraplength=350).place(x=15, y=35)

        btn_command = data.get("command", None)

        # Unified single conditional tracking for label text and button status
        if status == "Completed":
            btn_text = "Review"
            btn_state = NORMAL if btn_command else DISABLED
            status_text = "Completed"
            status_x = 400
        elif status == "Unlocked":
            btn_text = "Start"
            btn_state = NORMAL if btn_command else DISABLED
            status_text = "Available"
            status_x = 405
        else:
            btn_text = "Locked"
            btn_state = DISABLED
            status_text = "🔒 Locked"
            status_x = 495 

        if status != "Locked":
            btn = ttk.Button(
                self, 
                text=btn_text, 
                style="H6.TButton", 
                command=btn_command, 
                state=btn_state
            )
            btn.place(x=495, y=18, width=120, height=35)

        ttk.Label(self, text=status_text, style="HS4.TLabel").place(x=status_x, y=24)


        '''# questions and numbers (tooooo messy)
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

        self.overall = ttk.Label(self, text=" OVERALL PROGRESS", style="HS5.TLabel", anchor='nw')
        self.overall.place(x=30, y=120, width=680, height=90)

        # ---------------------------------------------------------------------!!!

        self.continue_last = ttk.Label(self, text="", style="HS5.TLabel", anchor='nw')
        self.continue_last.place(x=30, y=120, width=680, height=90)

        # ---------------------------------------------------------------------!!!

        self.profile_settings = ttk.Label(self, text="", style="HS5.TLabel", anchor='nw')
        self.profile_settings.place(x=740, y=60, width=525, height=110)


        #CRUD!!!'''