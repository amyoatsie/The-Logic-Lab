#from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM - hasn't really been used, remove?
import ttkbootstrap as ttk # type: ignore
#from ttkbootstrap.scrolled import ScrolledText - no longer used
from PIL import Image, ImageTk
from pathlib import Path

from models.challenge_evaluator import ChallengeEvaluator
from screens.custom_popup import ResultPopup
READONLY = "readonly" # Tkinter combobox state constant

class ChallengeScreenOne(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    # Displays the first digital forensics challenge.
    def __init__(self, parent, app):
        super().__init__(parent) # Initialise the frame inside the parent container (app.py)
        self.app = app

        SCREENS_DIR = Path(__file__).resolve().parent
        DATA_DIR = SCREENS_DIR.parent / "data"
        csv_path = DATA_DIR / "progress.csv"
        self.evaluator = ChallengeEvaluator(csv_path) # pass csv path into challenge evaluator

        IMAGE_NAMES = ["errorLevel", "luminanceGradient", "differenceAnalysis", "imageInfo"] # Image list ??? stored as a constant as it is never modified
        
        # Initialise an empty dictionary to store 'PhotoImage' objects and allow simplify retrieval
        self.icons = {}

        for name in IMAGE_NAMES:
            img_path = DATA_DIR / f"{name}.png"
            raw_img = Image.open(img_path)
            raw_img.thumbnail((520, 315))
            self.icons[name] = ImageTk.PhotoImage(raw_img) # Save it into the dictionary using its name as the key

    #----------------------------------------------------------------------------

        QUESTION_DATA = [ # Centralised list of dictionaries to allow for easier editing - stored as a constant because it is never modified
            {"text": "What does the outline around the objects primarily suggest?",
                "options": ["Image editing", "Camera blur", "Motion blur", "AI"]},
            {"text": "What section of the screen shows compression inconsistencies?",
                "options": ["Top", "Middle", "Bottom"]},
            {"text": "What does difference analysis compare?",
                "options": ["Image to File Data", "JPEG to PNG", "Metadata to GPS"]},
            {"text": "What were the original colours of the objects which were added in the altered image?",
                "options": ["Red & Green", "Blue & Yellow", "Orange & Green", "Pink & Blue"]}]

    #----------------------------------------------------------------------------

        self.title = ttk.Label(self, text="Metadata Analysis | Case 1", style="H1.TLabel", anchor='w') # change the heading to forensics cause more so image forensics than metadata now?
        self.title.place(x=30, y=40)

        self.explain = ttk.Label(self, text="""The first challenges revolves around the idea of forensic analysis. This challenge features four screens which can be viewed by clicking the labels on the right, and each question will correspond primarily to the figure with the same number.\n~
Figure 1.1 ~ Helps identify altered objects by showing inconsistent noise patterns.
Figure 1.2 ~ Helps expose pasted objects as they glow brighter than the original image.
Figure 1.3 ~ Helps highlight altered objects by visualizing hidden file changes.
Figure 1.4 ~ Additional background information.""", 
                                style="H4.TLabel", anchor='w', justify="left", wraplength=680)
        self.explain.place(x=30, y=120)
        # Question title
        self.question_header = ttk.Label(self, text="Questions", style="H2-2.TLabel", anchor='w')
        self.question_header.place(x=30, y=275, width=150, height=70)

        # Questions and numbers
        self.answer_boxes = []
        start_y = 330

        for i, question in enumerate(QUESTION_DATA):
            y = start_y + (i * 80)

            ttk.Label(self, text=f"{i+1})", style="H2.TLabel", anchor="w"
                    ).place(x=30, y=y, width=40, height=70)
            ttk.Label(self, text=question["text"], style="H3.TLabel", anchor="w", justify="left", wraplength=450
                    ).place(x=70, y=y, width=640, height=70)

            combo = ttk.Combobox(self, style="H4.TCombobox", values=question["options"], state=READONLY)
            combo.place(x=530, y=y+20, width=160, height=30)
            self.answer_boxes.append(combo)

    #----------------------------------------------------------------------------

        # Create and place comboboxes to simplify interface
        '''self.userAnswer1 = ttk.Combobox(self, style="H4.TCombobox", values=QUESTION_DATA[0]["options"], state=READONLY) # might move under each question?
        self.userAnswer1.place(x=530, y=350, width=160, height=30)
        self.userAnswer2 = ttk.Combobox(self, style="H4.TCombobox", values=QUESTION_DATA[1]["options"], state=READONLY)
        self.userAnswer2.place(x=530, y=430, width=160, height=30)
        self.userAnswer3 = ttk.Combobox(self, style="H4.TCombobox", values=QUESTION_DATA[2]["options"], state=READONLY)
        self.userAnswer3.place(x=530, y=510, width=160, height=30)
        self.userAnswer4 = ttk.Combobox(self, style="H4.TCombobox", values=QUESTION_DATA[3]["options"], state=READONLY)
        self.userAnswer4.place(x=530, y=590, width=160, height=30)'''

        # Create a submission button
        self.submit_button = ttk.Button(self, text="Submit", style="H6.TButton", command=self.on_submit_click) #Link the submit_button to the relevant command
        self.submit_button.place(x=910, y=590, width=220, height=52)

        self.home_button = ttk.Button(self, text="Home", style="H6.TButton", command=self.go_home)
        self.home_button.place(x=1190, y=30, width=80, height=45) 

    #----------------------------------------------------------------------------
        # Display an image and caption inside each Notebook tab

        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=720, y=120, width=580, height=410)

        self.tab_luminance = ImageTab(self.notebook, self.icons["luminanceGradient"],
        "Luminance Gradient | shows variations in brightness (luminance) across an image to expose physical inconsistencies")

        self.tab_error = ImageTab(self.notebook, self.icons["errorLevel"],
        "Error Level Analysis (ELA) | highlights differences in image quality from saving a JPEG (compressing an image)")

        self.tab_difference = ImageTab(self.notebook, self.icons["differenceAnalysis"],
        "Difference Analysis | compares a photo against its own hidden 'original thumbnail' to reveal hidden changes")

        self.tab_info = ImageTab(self.notebook, self.icons["imageInfo"],
        "Image Info | Additional background information on how the image was changed")

        self.notebook.add(self.tab_luminance, text=" Luminance Gradient ")
        self.notebook.add(self.tab_error, text=" Error Level Analysis ")
        self.notebook.add(self.tab_difference, text=" Difference Analysis ")
        self.notebook.add(self.tab_info, text="  Image Info  ") # spaces act as internal button padding

    #----------------------------------------------------------------------------

    def go_home(self): # Return the user to the home screen
        from screens.home_screen import HomeScreen # Import here as it creates a circular import if at the start
        self.app.show_screen(HomeScreen)

    # create functions/methods for the buttons inside the class? - should i move this to app or something else?
    def on_submit_click(self): # Fetch the active username and fall back to "Guest" if None
        #print("Submit button clicked!") # (from testing) add navigation in different folder?
        current_username = self.app.get_current_username()

        '''user_selections = {
            "q1": self.userAnswer1.get(), 
            "q2": self.userAnswer2.get(),
            "q3": self.userAnswer3.get(), 
            "q4": self.userAnswer4.get()
            }''' # from old design
        user_selections = {
            f"q{i+1}": answer.get()
            for i, answer in enumerate(self.answer_boxes)
            }

        is_valid, error_message = self.evaluator.validate_inputs(user_selections)
    
        if not is_valid:
            ResultPopup(self, "Incomplete Answers", error_message)
            return

        results = self.evaluator.evaluate_answers(user_selections)
        #print(results) # testing
        if current_username is not None:
            self.evaluator.save_progress(
                        username=current_username,  
                        challenge_name="Case 1",
                        score=results["score"], 
                        total=results["total"], 
                        passed=results["passed"]
                        )

        if results["passed"]:
            if current_username is None:
                ResultPopup(self, "Challenge Complete", 
                    f"Congratulations! You scored 100%. \nSign in to save progress/continue.")
            else:
                ResultPopup(self, "Challenge Complete", 
                                    f"Congratulations!\nYou scored {results['score']}/{results['total']}.", button_text="Continue")

                '''if hasattr(self.app, 'home_screen'):
                    self.app.home_screen.reload_user_state()
                    self.app.home_screen.create_widgets()'''
                
                from screens.home_screen import HomeScreen # Import here as it creates a circular import if at the start
                self.app.show_screen(HomeScreen)
        else:
            ResultPopup(self, "Challenge Complete",
                f"You scored {results['score']}/{results['total']}.\nTry again!")

    #----------------------------------------------------------------------------

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