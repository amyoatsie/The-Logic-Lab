import sys
from pathlib import Path
if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ttkbootstrap.constants import * # type: ignore # Import constants
import ttkbootstrap as ttk # type: ignore 
from models.challenge_evaluator import ChallengeEvaluator
from screens.custom_popup import ResultPopup
from  screens.case_one import ChallengeScreenOne
from repos.challenge_progress_repo import ChallengeProgressRepo

READONLY = "readonly"

    #----------------------------------------------------------------------------

class HomeScreen(ttk.Frame): # Display the main menu, user progress and available challenges through the GUI screen
    '''
Displays the main Logic Lab interface, including authentication, challenge progress, challenge cards and navigation 
to available cases.
    '''
    def __init__(self, parent: ttk.Frame, app):
        '''
    Args:
        parent (ttk.Frame) is the parent Tkinter frame in which this screen is displayed
            - A ttk.Frame is used because the screen is a graphical container for the child widgets.
        app (App) is the main application instance used to navigate between screens and access shared application 
        data such as the current username.
        '''
        super().__init__(parent) # Initialise this screen inside the app's navigation container
        self.app = app # Store the controller for navigation and user state

        self.csv_path = self.app.data_dir / "progress.csv"
        self.progress_repo = ChallengeProgressRepo(self.csv_path) # Repository handles reading and writing challenge progress

    #----------------------------------------------------------------------------

        # Initialise the screen's local progress state before loading saved user data
        self.total_challenges = 4
        self.completed_cases = set()
        self.completed_count = 0
        self.current_case_id = 1
        self.current_case_sub_progress = 0
        self.max_sub_challenges = 4

    #----------------------------------------------------------------------------

        # Store challenge metadata as a list of dictionaries for easier editing and to increase readability for future development
        # A list preserves the challenge order, while dictionaries group each challenge's ID, title, description and optional navigation command
        self.case_definitions = [ 
            {"id": 1, "title": "Case 01 | Metadata Analysis",
                "description": "Understading hidden information in files", "command": lambda: self.app.show_screen(ChallengeScreenOne)},
            {"id": 2, "title": "Case 02 | Digital Forensic Analysis",
                "description": "Analysing evidence and reconstructing events"}, # FUTURE DEV: Add commands when screens are created
            {"id": 3, "title": "Case 03 | Social Engineering",
                "description": "Phishing, impersonation, & manipulation tactics"},
            {"id": 4, "title": "Case 04 | Cryptography",
                "description": "Encryption, hashing, & secure communication"}
                ]
    
        # StringVars allow the displayed username and authentication button text to be updated when the user's login state changes
        self.username_var = ttk.StringVar()
        self.auth_button_var = ttk.StringVar()

        # Read and load saved progress for the current user before creating the interface
        self.reload_user_state()
        self.create_widgets()

    #----------------------------------------------------------------------------

    def reload_user_state(self): # Load the current user's saved progress and update the screen state
        current_user = self.app.get_current_username() # Retrieve the username
        
        if current_user:
            self.username_var.set(f"Welcome Back, {current_user}")
            self.auth_button_var.set("Sign Out")
        
            # Request completed challenge IDs from the repo rather than accessing the CSV directly from the screen
            self.completed_cases = self.progress_repo.get_completed_cases(current_user)
        
        else:
            self.username_var.set("Welcome to Logic Lab, Guest")
            self.auth_button_var.set("Sign In / Up")
            self.completed_cases = set()

        self.completed_count = len(self.completed_cases)
        
        # Unlock the first incomplete challenge while preventing the challenge ID from exceeding the total number of available challenges
        if not self.completed_cases:
            self.current_case_id = 1
        else:
            self.current_case_id = min(max(self.completed_cases) + 1, self.total_challenges)

        active_idx = self.current_case_id - 1
        self.current_case_title = self.case_definitions[active_idx]["title"]

    #----------------------------------------------------------------------------

    def validate_username(self, username: str) -> tuple[bool, str | None]: # Validate the format and length of a username before signing the user in
        '''
    Args:
        username (str) is the username entered into the login popup
            - A string is used because usernames are entered and stored as text.
    ~
    Returns:
        tuple: Contains a boolean indicating whether the username is valid and a string containing 
        an error message if validation fails.
            - A tuple groups the validation result and relevant error message.
            - A boolean indicates whether the username passed validation.
            - A string stores the error message displayed to the user.
            - None is returned when no error message is required.
        '''
        username = username.strip()

        if len(username) < 1: # Reject usernames which are less than 1 character long
            return False, "Invalid access attempt! Please enter a username that is at least 1 character long."
        if len(username) > 25: # Reject usernames which are over 25 characters long
            return False, "Invalid access attempt! Username must be less than or equal to 25 characters."
        if username[0].isdigit(): # Reject usernames beginning with a digit
            return False, "Invalid access attempt! Your username cannot start with a number."
        return True, None

    #----------------------------------------------------------------------------

    def handle_auth_action(self): # Toggle login state and refresh the displayed user
        current_user = self.app.get_current_username() 
        
        if current_user:
            # Sign out by clearing the current user
            self.app.current_user = None
            self.reload_user_state()
            self.create_widgets()
        else:
            # Launch the custom text entry popup window to request a username
            popup = ResultPopup(
                parent=self,
                title="System Login",
                message="Enter your username or undercover alias:",
                button_text="Submit",
                show_input=True
                )
            # Validate that the username exists
            if popup.user_input_value is not None:
                input_name = popup.user_input_value.strip()
                is_valid, error_message = self.validate_username(input_name)

                if not is_valid: # Reject usernames which don't pass validation
                    ResultPopup(
                        parent=self,
                        title="Access Denied",
                        message=error_message,
                        button_text="Try Again",
                        show_input=False
                        )
                    return

                self.app.current_user = input_name
                self.reload_user_state()
                self.create_widgets()

    #----------------------------------------------------------------------------

    def handle_reset_progress(self): # Confirm and reset the current user's saved challenge progress
        # Use the custom ResultPopup as a confirmation dialog/popup first
        current_user = self.app.get_current_username() # Normalise the username so it matches the format used by the repo
    
        if not current_user:
            return

        current_user = current_user.strip().lower()
        
        popup = ResultPopup(
            parent=self,
            title="Reset Progress?",
            message="Are you sure you want to clear your data? This will reset your progress and lock all cases except for case 1.",
            button_text="Confirm Reset",
            show_input=False
        )

        if not popup.confirmed: # Stop if the user cancels or closes the confirmation popup
            return

        try:
            self.progress_repo.reset_user_progress(current_user) # Repo handles deletion of the user's CSV records

            # Reset the screen's local progress state after the saved records are removed
            self.completed_cases = set()
            self.completed_count = 0
            self.current_case_id = 1
            self.current_case_title = "Case 01 | Metadata Analysis"
            
            # Refresh the displayed information
            self.reload_user_state()
            self.create_widgets()
            
        except Exception as e:
            print(f"Error resetting progress: {e}")

    #----------------------------------------------------------------------------

    def create_widgets(self): # Create the HomeScreen interface based on the current user and progress
        for child in self.winfo_children(): # Remove existing widgets before rebuilding the screen
            child.destroy()

        self.title = ttk.Label(self, textvariable=self.username_var, style="H1.TLabel")
        self.title.place(x=30, y=40)

        progress = ttk.Frame(self, style="Card.TFrame", padding=15)
        progress.place(x=30, y=120, width=650, height=120)

        ttk.Label(progress, text="OVERALL PROGRESS", style="HS5.TLabel").pack(anchor="w")

        # Display the number of completed challenges using the current progress state
        self.progress = ttk.Progressbar(progress, maximum=self.total_challenges, 
            value=self.completed_count, style="Logic.Horizontal.TProgressbar")
        self.progress.pack(fill=X, pady=12)

        ttk.Label(progress, 
            text=f"{self.completed_count} / {self.total_challenges} Challenges Completed", 
            style="H5.TLabel").pack(anchor="e")

        # Create right Panels
        self.create_continue_card()
        self.create_profile_card()

        # Iterate through the challenge definitions and create a card for each case
        start_y = 270
        for config in self.case_definitions: # Determine each challenge's
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

        # Display progress within the currently active challenge
        ttk.Progressbar(
            frame, 
            maximum=self.max_sub_challenges, 
            value=self.current_case_sub_progress, 
            style="Logic.Horizontal.TProgressbar"
            ).pack(fill=X, pady=10)

        active_idx = self.current_case_id - 1
        active_command = self.case_definitions[active_idx].get("command", None) # Retrieve the navigation command
        button_state = NORMAL if active_command else DISABLED

        ttk.Button(frame, text="Continue", style="H6.TButton", 
                command=active_command, state=button_state).pack(anchor="w")

    #----------------------------------------------------------------------------

    def create_profile_card(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        frame.place(x=720, y=300, width=550, height=80)

        ttk.Label(frame, text="PROFILE SETTINGS", style="HS5.TLabel").place(x=15, y=14)

        # Allow the button to change between "Sign In / Up" and "Sign Out"
        self.auth_button = ttk.Button(
            frame, 
            textvariable=self.auth_button_var, 
            style="H6.TButton", 
            command=self.handle_auth_action
        )
        self.auth_button.place(x=235, y=8, width=120, height=35)

        # Deactivate reset options while the user is a 'Guest'
        is_logged_in = self.app.get_current_username() is not None
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

class CaseCard(ttk.Frame): # Reusable GUI component used to display a challenge case
    def __init__(self, parent, case_data, status):
        '''
    Args:
        parent (ttk.Frame) is the parent GUI frame that the CaseCard is placed inside
            - A ttk.Frame is used because the CaseCard is a GUI component displayed within another frame.
        case_data (dict) is a dictionary containing the challenge's ID, title, description and command
            - A dictionary is used because multiple related pieces of challenge information need to be 
            stored together and accessed using clear/descriptive keys.
        status (str) is the current status of the challenge, (e.g. "Completed", "Unlocked" or "Locked")
            - A string is used because the status is represented by a text value.
        '''
        super().__init__(parent, padding=10, style="Card.TFrame")

        ttk.Label(self, text=case_data["title"], style="HS2.TLabel", wraplength=380).place(x=15, y=5)
        ttk.Label(self, text=case_data["description"], style="HS4.TLabel", wraplength=350).place(x=15, y=35)

        button_command = case_data.get("command", None) # Retrieve the challenge's navigation command, if one exists

        # Configure the button, status text and availability based on the challenge status
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
            status_text = "🔒 Locked" # The emoji is much easier to add then an actual image
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