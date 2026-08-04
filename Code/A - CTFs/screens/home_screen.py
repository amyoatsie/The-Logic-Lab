import sys
import csv
from pathlib import Path
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ttkbootstrap.constants import * # type: ignore # Import constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore 
from models.challenge_logic import ChallengeEvaluator
from screens.custom_popup import ResultPopup

READONLY = "readonly"

class HomeScreen(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page MAKE 'h' CAPS
    def __init__(self, parent, app):
        super().__init__(parent) # Initialise the frame inside the parent container (app.py)
        self.app = app

        SCREENS_DIR = Path(__file__).resolve().parent
        DATA_DIR = SCREENS_DIR.parent / "data"
        self.csv_path = DATA_DIR / "progress.csv"
        #self.config_path = DATA_DIR / "config.txt"
        
        self.ensure_csv_exists()
        self.evaluator = ChallengeEvaluator(self.csv_path) # Parse csv path into challenge evaluator

    #----------------------------------------------------------------------------

        # Default progress state (set defaults to run at the START not the end in case of crashes, to prevent orphaned data)
        self.total_challenges = 4
        self.completed_cases = set()
        self.completed_count = 0
        self.current_case_id = 1
        self.current_case_sub_progress = 0
        self.max_sub_challenges = 4

    #----------------------------------------------------------------------------

        self.case_definitions = [ # Centralised list of dictionaries to allow easier editing & increase readability for future development
            {"id": 1, "title": "Case 01 | Metadata Analysis",
                "description": "Understading hidden information in files", "command": self.app.show_case_one},
            {"id": 2, "title": "Case 02 | Digital Forensic Analysis",
                "description": "Analysing evidence and reconstructing events"}, #add command when screen is created
            {"id": 3, "title": "Case 03 | Social Engineering",
                "description": "Phishing, impersonation, & manipulation tactics"},
            {"id": 4, "title": "Case 04 | Cryptography",
                "description": "Encryption, hashing, & secure communication"}
                ]
    
        # Load user tracking
        self.username_var = ttk.StringVar()
        self.auth_button_var = ttk.StringVar()

        # Read & extract history logs
        self.reload_user_state()
        self.create_widgets()

    #----------------------------------------------------------------------------

    def ensure_csv_exists(self): # Build table headers if CSV is empty/doesn't exist
        if not self.csv_path.exists():
            try:
                self.csv_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["username", "timestamp", "currentChallenge", "numberCorrect", "questionNumber", "result"]) # Header row
            except Exception:
                pass

    #----------------------------------------------------------------------------

    def load_username(self): # Load user profile (not sure if this actually does anything rn?)
        if hasattr(self.app, 'current_user') and self.app.current_user:
            return self.app.current_user.strip()
        return None

    #----------------------------------------------------------------------------

    def reload_user_state(self): # Extract progress based on the current user
        current_user = self.load_username()
        
        if current_user:
            self.username_var.set(f"Welcome Back, {current_user}")
            self.auth_button_var.set("Sign Out")
        
            # Filter and parse data for this user
            self.completed_cases = self.get_completed_cases_from_csv(self.csv_path, current_user)
        
        else:
            self.username_var.set("Welcome to Logic Lab, Guest")
            self.auth_button_var.set("Sign In")
            self.completed_cases = set()

        self.completed_count = len(self.completed_cases)
        
        if not self.completed_cases:
            self.current_case_id = 1
        else:
            self.current_case_id = min(max(self.completed_cases) + 1, self.total_challenges)

        active_idx = self.current_case_id - 1
        self.current_case_title = self.case_definitions[active_idx]["title"]

    #----------------------------------------------------------------------------

    def handle_auth_action(self): # Toggle login state using the custom project popup window
        current_user = self.load_username() # Create a local variable for readability (might not be needed???)
        
        if current_user:
            # Sign Out logic: clear file contents and reset variables
            self.app.current_user = None
            self.reload_user_state()
            self.create_widgets()
        else:
            # Sign In logic: launch the custom text entry popup window
            popup = ResultPopup(
                parent=self,
                title="System Login",
                message="Enter your username or undercover alias:",
                button_text="Submit",
                show_input=True
            )
            # Save name if user provided a valid input string (existense validation)
            if popup.user_input_value and popup.user_input_value.strip():
                input_name = popup.user_input_value.strip()

                if input_name[0].isdigit(): # Type validation to check if the username STARTS with a number
                    ResultPopup(
                        parent=self,
                        title="Access Denied",
                        message="Invalid access attempt! Your username cannot start with a number.",
                        button_text="Try Again",
                        show_input=False
                    )
                    return

                self.app.current_user = input_name
                self.reload_user_state()
                self.create_widgets()

    #----------------------------------------------------------------------------

    def handle_reset_progress(self): # Wipe progress data from the CSV while keeping the header line
        # Use the custom ResultPopup as a confirmation dialog/popup first
        current_user = self.load_username()
    
        if not current_user:
            return
        
        popup = ResultPopup(
            parent=self,
            title="Reset Progress?",
            message="Are you sure you want to clear your data? This will reset your progress and lock all cases except for case 1.",
            button_text="Confirm Reset",
            show_input=False
        )

        if not popup.confirmed: # Exit early if the user closes the popup or clicks cancel
            return

        if not self.csv_path.exists(): # CRUD
            return
        
        try:
            # Read the existing CSV file
            with open(self.csv_path, "r") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                rows = list(reader)
                
            remaining_rows = [row for row in rows 
                            if row["username"] != current_user]
            
            fieldnames = ["username", "timestamp", "currentChallenge",
                "numberCorrect", "questionNumber", "result"]
        
            with open(self.csv_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(remaining_rows)

            # Reset the local variables back to 'default' states
            self.completed_cases = set()
            self.completed_count = 0
            self.current_case_id = 1
            self.current_case_title = "Case 01 | Metadata Analysis"
            
            # Update the UI components to refresh the screen
            self.reload_user_state()
            self.create_widgets()
            
        except Exception as e:
            print(f"Error resetting progress file logic tracks: {e}") # Error message

    #----------------------------------------------------------------------------

    def get_completed_cases_from_csv(self, path, username): # Read the progress CSV file to find successful cases
        completed = set()
    
        if not path.exists():
            return completed
        try:
            with open(path, "r", newline="") as f:
                reader = csv.DictReader(f)
            
                for row in reader:
                    if row["username"] != username:
                        continue
                
                    if row["result"].strip().lower() == "pass":
                        case_str = row["currentChallenge"]
                        num = int(''.join(filter(str.isdigit, case_str)
                            ))
                        completed.add(num)

        except Exception as e:
            print(f"Error reading progress: {e}")
    
        return completed

    #----------------------------------------------------------------------------

    def create_widgets(self):
        for child in self.winfo_children(): # Clear out any pre-existing widgets inside this frame container
            child.destroy()

        self.title = ttk.Label(self, textvariable=self.username_var, style="H1.TLabel")
        self.title.place(x=30, y=40)

        progress = ttk.Frame(self, style="Card.TFrame", padding=15)
        progress.place(x=30, y=120, width=650, height=120)

        ttk.Label(progress, text="OVERALL PROGRESS", style="HS5.TLabel").pack(anchor="w")

        # Link to total challenges completed
        self.progress = ttk.Progressbar(progress, maximum=self.total_challenges, 
            value=self.completed_count, style="Logic.Horizontal.TProgressbar")
        self.progress.pack(fill=X, pady=12)

        ttk.Label(progress, 
            text=f"{self.completed_count} / {self.total_challenges} Challenges Completed", 
            style="H5.TLabel").pack(anchor="e")

        # Create right Panels
        self.create_continue_card()
        self.create_profile_card()

        # Case Cards Setup Loop
        start_y = 270
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

    #----------------------------------------------------------------------------

    def create_continue_card(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        frame.place(x=720, y=120, width=550, height=170)

        ttk.Label(frame, text="CONTINUE LAST CHALLENGE", style="HS5.TLabel").pack(anchor="w")
        ttk.Label(frame, text=self.current_case_title, style="H3.TLabel").pack(anchor="w", pady=(10,0))

        # Update the progress bar to match the current completion level
        ttk.Progressbar(
            frame, 
            maximum=self.max_sub_challenges, 
            value=self.current_case_sub_progress, 
            style="Logic.Horizontal.TProgressbar"
        ).pack(fill=X, pady=10)

        active_idx = self.current_case_id - 1
        active_command = self.case_definitions[active_idx].get("command", None)
        button_state = NORMAL if active_command else DISABLED

        ttk.Button(frame, text="Continue", style="H6.TButton", 
                command=active_command, state=button_state).pack(anchor="w")

    #----------------------------------------------------------------------------

    def create_profile_card(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        frame.place(x=720, y=300, width=550, height=80)

        ttk.Label(frame, text="PROFILE SETTINGS", style="HS5.TLabel").place(x=15, y=14)

        # Allow the button to change between "Sign In" and "Sign Out"
        self.auth_button = ttk.Button(
            frame, 
            textvariable=self.auth_button_var, 
            style="H6.TButton", 
            command=self.handle_auth_action
        )
        self.auth_button.place(x=235, y=8, width=120, height=35)

        # Deactivate reset options if the user is unauthenticated ("Guest")
        is_logged_in = self.load_username() is not None
        reset_state = NORMAL if is_logged_in else DISABLED
        
        reset_button = ttk.Button(
            frame, 
            text="Reset Progress", 
            style="H6.TButton",
            command=self.handle_reset_progress,
            state=reset_state
        )
        reset_button.place(x=375, y=8, width=135, height=35)

    #----------------------------------------------------------------------------

class CaseCard(ttk.Frame):
    def __init__(self, parent, data, status):
        super().__init__(parent, padding=10, style="Card.TFrame")

        ttk.Label(self, text=data["title"], style="HS2.TLabel", wraplength=380).place(x=15, y=5)
        ttk.Label(self, text=data["description"], style="HS4.TLabel", wraplength=350).place(x=15, y=35)

        button_command = data.get("command", None)

        # Conditional tracking for label text (sign in vs out) and button status
        if status == "Completed":
            button_text = "Review"
            button_state = NORMAL if button_command else DISABLED
            status_text = "" # Show no text as it appears overwhelming
            status_x = 400
        elif status == "Unlocked":
            button_text = "Start"
            button_state = NORMAL if button_command else DISABLED
            status_text = ""
            status_x = 405
        else:
            button_text = "Locked"
            button_state = DISABLED
            status_text = "🔒 Locked" # the emoji is much easier to add then an actual image
            status_x = 495 

        if status != "Locked":
            button = ttk.Button(
                self, 
                text=button_text, 
                style="H6.TButton", 
                command=button_command, 
                state=button_state
            )
            button.place(x=495, y=18, width=120, height=35)

        ttk.Label(self, text=status_text, style="HS4.TLabel").place(x=status_x, y=24)