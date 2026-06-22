from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore CHANGE SCREEN NAME LMAO
from ttkbootstrap.scrolled import ScrolledText
from PIL import Image, ImageTk
from pathlib import Path

class challengeScreenOne(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)

        SCREENS_DIR = Path(__file__).resolve().parent
        DATA_DIR = SCREENS_DIR.parent / "data"

        errorLevelPath = DATA_DIR / "errorLevel.png"
        luminanceGradientPath= DATA_DIR / "luminanceGradient.png"
        differenceAnalysisPath = DATA_DIR / "differenceAnalysis.png"
        #errorLevelPath = DATA_DIR / "differenceAnalysis.png" ADD MAP

        errorLevelImage = Image.open(errorLevelPath)
        self.errorLevel_icon = ImageTk.PhotoImage(errorLevelImage)
    
        luminanceGradientImage = Image.open(luminanceGradientPath)
        self.luminanceGradient_icon = ImageTk.PhotoImage(luminanceGradientImage)

        differenceAnalysisImage = Image.open(differenceAnalysisPath)
        self.differenceAnalysis_icon = ImageTk.PhotoImage(differenceAnalysisImage)

        #-------------------------------
        
        question_one = ["Australia", "Canada", "Germany", "Japan"] # change these lol
        question_two = ["Chloe", "Bob", "Patrick", "Jane"]
        question_three = ["Methods", "Literature", "Physics", "Software"]
        question_four = ["Cake", "Ice Cream", "Cookie", "Brownie"]

        #---------------------------------

        self.title = ttk.Label(self, text="Metadata Analysis | Case 1", style="H1.TLabel", anchor='w') #inverse will make the background that colour rather than the text
        self.title.place(x=30, y=30) #15 minutes into video...

        self.explain = ttk.Label(self, text="The first challenges revolves around the idea of forensic analysis. This ???", style="H4.TLabel", anchor='w')
        self.explain.place(x=30, y=100) #might move questions up and extend notebook height for text? ADD EXPLAIN

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
        self.button_try.place(x=915, y=545, width=220, height=52) # might inverse colouring? (to match the primary and highlight as info)

        # ---------------------------------------------------------------------!!!

        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=720, y=120, width=580, height=350)
        
        # Instantiate the tab frames inside the notebook container
        self.tab_metadata = metaDataTab(self.notebook)
        self.tab_noise = noiseAnalysisTab(self.notebook)
        self.tab_clone = cloneDetectionTab(self.notebook)
        self.tab_error = errorLevelTab(self.notebook)
        
        # Mount them as bottom tabs (to match the mockup)
        self.notebook.add(self.tab_metadata, text="Meta Data")
        self.notebook.add(self.tab_noise, text="Noise Analysis")
        self.notebook.add(self.tab_clone, text="Clone Detection")
        self.notebook.add(self.tab_error, text="Error Level")

        '''# Right Panel Notebook System
        self.notebook = ttk.Notebook(self, style='bottomtab.TNotebook')
        self.notebook.place(x=754, y=188, width=582, height=351)
        
        # Fetching the data directory handle defined in your App window class wrapper
        # self.master is your container, self.master.master is your App instance
        app_instance = self.master.master
        images_dir = app_instance.data_dir / "images" # Assumes your images live inside your data folder
        
        # --- THE FIX: Instantiate our reusable image tabs with unique asset paths! ---
        self.tab_metadata = ImageTab(self.notebook, images_dir / "gps_map.png", "GPS Navigation Target Context")
        self.tab_noise = ImageTab(self.notebook, images_dir / "noise_chart.png", "Frequency Noise Levels")
        self.tab_clone = ImageTab(self.notebook, images_dir / "clone_matrix.png", "Visual Clone Detection Overlay")
        self.tab_error = ImageTab(self.notebook, images_dir / "error_map.png", "Error Level Analysis Stream")
        
        # Mount them as the clean bottom tabs matching your design layout
        self.notebook.add(self.tab_metadata, text="Meta Data")
        self.notebook.add(self.tab_noise, text="Noise Analysis")
        self.notebook.add(self.tab_clone, text="Clone Detection")
        self.notebook.add(self.tab_error, text="Error Level")'''

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

#--------------------------------------------

class noiseAnalysisTab(ttk.Frame):
    """The workspace view that displays inside the 'Noise Analysis' notebook tab."""
    def __init__(self, parent):
        super().__init__(parent, style='TFrame')
        
        #lbl = ttk.Label(self, text="GPS Navigation Target Context", style='H3.TLabel')
        #lbl.pack(anchor=NW, padx=15, pady=15) (a title but not needed?")
        
        self.console = ScrolledText(self, padding=5, autohide=True, )
        self.console.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.console.insert(END, "Awaiting submission execution data...") #change

#--------------------------------------------

class cloneDetectionTab(ttk.Frame):
    """The workspace view that displays inside the 'Noise Analysis' notebook tab."""
    def __init__(self, parent):
        super().__init__(parent, style='TFrame')
        
        #lbl = ttk.Label(self, text="GPS Navigation Target Context", style='H3.TLabel')
        #lbl.pack(anchor=NW, padx=15, pady=15) (a title but not needed?")
        
        self.console = ScrolledText(self, padding=5, autohide=True, )
        self.console.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.console.insert(END, "Awaiting submission execution data...") #change

#--------------------------------------------

class errorLevelTab(ttk.Frame):
    """The workspace view that displays inside the 'Noise Analysis' notebook tab."""
    def __init__(self, parent):
        super().__init__(parent, style='TFrame')
        
        #lbl = ttk.Label(self, text="GPS Navigation Target Context", style='H3.TLabel')
        #lbl.pack(anchor=NW, padx=15, pady=15) (a title but not needed?")
        
        self.console = ScrolledText(self, padding=5, autohide=True, )
        self.console.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.console.insert(END, "Awaiting submission execution data...") #change


#----------------------------------------------------!!!

class ImageTab(ttk.Frame):
    """A modular tab that displays a resized image asset seamlessly."""
    def __init__(self, parent, image_path, title_text):
        super().__init__(parent, style='TFrame')
        
        # 1. Text Title Header for the Tab content workspace
        lbl = ttk.Label(self, text=title_text, style='H3.TLabel')
        lbl.pack(anchor=NW, padx=15, pady=15)
        
        try:
            # 2. Open the raw image asset file using Pillow
            raw_img = Image.open(image_path)
            
            # 3. Resize the image to fit your exact Figma Notebook viewport safely
            # Notebook size is 582x351. Tab headers take ~35px, so ~550x300 works beautifully.
            resized_img = raw_img.resize((550, 280), Image.Resampling.LANCZOS)
            
            # 4. Convert the Pillow image into a format Tkinter understands
            self.tab_image = ImageTk.PhotoImage(resized_img)
            
            # 5. Drop the image inside a flat Label container to display it
            self.image_container = ttk.Label(self, image=self.tab_image, background=self.cget('style'))
            self.image_container.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))
        
        except Exception as e:
            # Fallback error block in case a path is wrong or missing during testing
            error_lbl = ttk.Label(self, text=f"Error loading image:\n{e}", style='H5.TLabel', foreground='red')
            error_lbl.pack(pady=50)