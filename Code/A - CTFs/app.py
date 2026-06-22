import tkinter as tk
from pathlib import Path
import ttkbootstrap as ttk # type: ignore (error showed)

# Import screens
from screens.home_screen import homeScreen
from screens.case_one import challengeScreenOne
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

        # initialize initial screen display !!! change to homescreen!
        self.current_screen = challengeScreenOne(self.container)
        self.current_screen.pack(fill="both", expand=True)

    def setup_custom_theme(self): # custom colouring is defined to match the mockups in a method
        # Creates and applies the global color set application-wide
        style = ttk.Style()
        custom_colors = {
            'primary': '#46403A',
            'secondary': '#D7C4AC',
            'success': "#61daae", 
            'info': '#A2B9CB', # same as border
            'warning': '#f6c23e', # might not need to change?
            'danger': '#B3261E',
            'light': '#FFF6EB',
            'dark': '#5a5c69', # have yet to change
            'bg': '#C1A37F',
            'fg': '#2e2f37', # have yet to change, text colour (fg)
            'selectbg': '#eaecf4', # have yet to change
            'selectfg': "#ffffff", # front 
            'border': '#A2B9CB',
            'inputfg': '#2e2f37', # have yet to change
            'inputbg': '#CAB8A2',
            'active': '#dddfeb' # have yet to change
            }
        
        style.theme_names().append('logic_lab_theme')
        style.theme_use('flatly') # Set a standard base theme style to safely map basic window behaviors !!!        
        # Override the colors in memory instantly using the official settings setter
        for color_name, hex_code in custom_colors.items():
            style.colors.set(color_name, hex_code)

        HEADING_FONT = "Arial Black" # Used "Arial Black" as an Archivo alternative 
        BODY_FONT = "Roboto" # Main text font defined as a constant
        BG_COLOR = custom_colors['bg']

        # Heading 1 (The main header)
        style.configure('H1.TLabel', font=(HEADING_FONT, -48), foreground=custom_colors['primary'], 
                        background=BG_COLOR)
        # Heading 2 (The question numbers)
        style.configure('H2.TLabel', font=(BODY_FONT, -24), foreground=custom_colors['primary'], 
                        background=custom_colors['secondary'])
        # Heading 3 (The menu sub-headings and the questions)
        style.configure('H3.TLabel', font=(BODY_FONT, -18), foreground=custom_colors['primary'], 
                        background=custom_colors['secondary'])
        # Heading 4 (The user inputs and main answers) !!!
        style.configure('H4.TLabel', font=(BODY_FONT, -16), foreground=custom_colors['primary'], 
                        background=BG_COLOR)
        # Heading 5 (The explanatory text)
        style.configure('H5.TLabel', font=(BODY_FONT, -14), foreground=custom_colors['primary'], 
                        background=BG_COLOR)
        # Heading 6 (Buttons)
        style.configure('H6.TButton', font=(BODY_FONT, -16), foreground=custom_colors['light'], 
                        background=custom_colors['info'], bordercolor=custom_colors['border'], 
                        focuscolor=custom_colors['border']) # Outline border color and Focus ring color

    #----------------------------------------------------------------------------
        # Heading 7 (Comboboxes)
        style.configure('H4.TCombobox', font=(BODY_FONT, -16))

        # Combobox styling overrides (had to google)
        style.map('H4.TCombobox', # State Maps: This explicitly overrides operating system states to ensure it preserves the custom colours
            fieldbackground=[('readonly', custom_colors['light']), ('disabled', custom_colors['light'])],
            foreground=[('readonly', custom_colors['fg']), ('disabled', custom_colors['fg'])],
            selectbackground=[('readonly', custom_colors['light'])], # Keeps the selection block clean inside the field
            selectforeground=[('readonly', custom_colors['fg'])])
        # Popup colour overrides
        self.option_add('*TCombobox*Listbox.font', (BODY_FONT, -16)) # Changes the dropdown list font to match the combobox design
        def on_dropdown_popdown(event): # Register a class binding for every Combobox that manually forces the inner sub-listbox to accept custom colours
            popdown = event.widget.tk.call('ttk::combobox::PopdownWindow', event.widget) # !!!
            listbox = popdown + '.f.l'
            # Directly configure the underlying Tk graphic properties
            event.widget.tk.call(listbox, 'configure', '-background', custom_colors['light']) # Background color of the open dropdown menu list
            event.widget.tk.call(listbox, 'configure', '-foreground', custom_colors['primary']) # Text color of the unselected options inside the dropdown menu list
            event.widget.tk.call(listbox, 'configure', '-selectbackground', custom_colors['secondary']) # Highlight background color when you hover or arrow key down over an item
            event.widget.tk.call(listbox, 'configure', '-selectforeground', custom_colors['primary']) # Text color of the currently highlighted/selected option item
        self.bind_class('TCombobox', '<Map>', on_dropdown_popdown)  # Apply a listener configuration to all comboboxes instantiated

    #---------------------------------------------------------------------------
        #Tabs
        
        # Create a custom notebook style targeting the bottom orientation
        style.configure('bottomtab.TNotebook', 
                        background=custom_colors['bg'], 
                        tabposition='s',
                        borderwidth=0,
                        highlightthickness=0,
                        lightcolor=custom_colors['bg'],
                        darkcolor=custom_colors['bg'],
                        bordercolor=custom_colors['bg'])
        
        style.layout('bottomtab.TNotebook.Tab', [
            ('Notebook.tab', {'sticky': 'nswe', 'children': [
                ('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [
                    ('Notebook.label', {'side': 'top', 'sticky': ''})
                ]})
            ]})
        ])
        
        # Style the tab header buttons at the bottom
        style.configure('bottomtab.TNotebook.Tab', 
                        background=custom_colors['secondary'], 
                        foreground=custom_colors['primary'], 
                        padding=[15, 6], 
                        font=(BODY_FONT, 10, 'bold'),
                        borderwidth=0,
                        focuscolor=custom_colors['bg'],
                        bordercolor=custom_colors['bg'])
        
        # Preserve color map changes for the bottom tab headers
        style.map('bottomtab.TNotebook.Tab', 
                    background=[
                    ('selected', custom_colors['primary']), 
                    ('active', custom_colors['active'])
                ], 
                foreground=[
                    ('selected', custom_colors['light']), 
                    ('active', custom_colors['fg'])
                ],
                bordercolor=[
                    ('selected', custom_colors['bg']),
                    ('active', custom_colors['bg']),
                    ('focus', custom_colors['bg'])
                ],
                lightcolor=[
                    ('selected', custom_colors['bg']),
                    ('focus', custom_colors['bg'])
                ],
                darkcolor=[
                    ('selected', custom_colors['bg']),
                    ('focus', custom_colors['bg'])
                ])

#------------------------------------------------------------------------------

    # write navigation functions here (idk if they should be inside or outside of class?)
    def switch_screen(self, new_screen_class):
        """Swaps the current screen view out cleanly for another."""
        if self.current_screen is not None:
            self.current_screen.destroy()
        
        self.current_screen = new_screen_class(self.container)
        self.current_screen.pack(fill="both", expand=True)

def run(self):#method for mainloop
    self.mainloop()
