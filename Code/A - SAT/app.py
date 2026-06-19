import tkinter as tk
from pathlib import Path
import ttkbootstrap as ttk # type: ignore (error showed)

# Import screens
from screens.home_screen import HomeScreen
# e.g. from screens.challenge_1 import Challenge1Screen (might change the name?)

# Import repos
# e.g. from repos.challenge_repo_csv import ChallengeRepoCsv


class App(ttk.Window): # Inherit directly from ttk.Window instead of standard tk.Tk
    def __init__(self):
        super().__init__(title="User Module Access", size=(1366, 768))

        #variables defined inside app class, therefore references as "app.___"
        self.base_dir = Path(__file__).resolve().parent #references the "relative folder"!!!
        self.data_dir = self.base_dir / "data" #act like global variables but are only defined once

        self.setup_custom_theme() # injects global style engine profile

        # define repos
        # e.g. self.challenge_repo = ChallengeRepoCsv(self.data_dir / "progress.csv")

        # define Navigation Container (Where screens swap out) !!!
        self.container = ttk.Frame(self) # in case future errors occur, ttk could be change to tb which is a more universal abbreviation
        self.container.pack(fill="both", expand=True)

        # initialize initial screen display !!!
        self.current_screen = HomeScreen(self.container)
        self.current_screen.pack(fill="both", expand=True)

    def setup_custom_theme(self): # custom colouring is defined to match the mockups
        # Creates and applies the global color set application-wide
        style = ttk.Style()
        custom_theme_data = {
            "name": "logic_lab_theme",
            "type": "light",
            "colors": {
            'primary': '#46403A',
            'secondary': '#D7C4AC',
            'success': "#61daae", 
            'info': '#36b9cc', # might not need to change?
            'warning': '#f6c23e', # might not need to change?
            'danger': '#B3261E',
            'light': '#FFF6EB',
            'dark': '#5a5c69', # have yet to change
            'bg': '#C1A37F',
            'fg': '#2e2f37', # have yet to change, text colour (fg)
            'selectbg': '#eaecf4', # have yet to change
            'selectfg': '#2e2f37', # have yet to change
            'border': '#A2B9CB',
            'inputfg': '#2e2f37', # have yet to change
            'inputbg': '#ffffff', # have yet to change
            'active': '#dddfeb' # have yet to change
            }
        }
        from ttkbootstrap.themes.standard import ThemeDefinition # Used google to fix the theme_name error with this
        custom_theme = ThemeDefinition(
            name=custom_theme_data["name"],
            themetype=custom_theme_data["type"],
            colors=custom_theme_data["colors"]
        )

        style.register_theme(custom_theme)
        style.theme_use(custom_theme.name)
        



    # write navigation functions here (idk if they should be inside or outside of class?)
    def switch_screen(self, new_screen_class):
        """Swaps the current screen view out cleanly for another."""
        if self.current_screen is not None:
            self.current_screen.destroy()
        
        self.current_screen = new_screen_class(self.container)
        self.current_screen.pack(fill="both", expand=True)

def run(self):#method for mainloop
    self.mainloop()
