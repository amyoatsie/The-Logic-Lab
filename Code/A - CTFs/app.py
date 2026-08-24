from pathlib import Path
import ttkbootstrap as ttk # type: ignore

from screens.home_screen import HomeScreen
from screens.case_one import ChallengeScreenOne # ???

# Global constants used to maintain consistent typography and window dimensions
HEADING_FONT = "Arial Black" # Main heading font defined for clarity
BODY_FONT = "Roboto" # Main body font defined for clarity
WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768

    #----------------------------------------------------------------------------

class App(ttk.Window): # Allow the main application controller to inherit directly from ttk.Window
    # Control the main app window, theme and screen navigation
    def __init__(self):
        super().__init__(title="User Module Access", size=(WINDOW_WIDTH, WINDOW_HEIGHT))

        # Store the current user, with 'None' representing a guest
        self.current_user = None

        # Store paths relative to the directory so the program can locate the files regardless of the launch location
        self.base_dir = Path(__file__).resolve().parent 
        self.data_dir = self.base_dir / "data"

        # Apply the custom visual theme and widget styles
        self.setup_custom_theme()

        # Define Navigation Container used as the parent for the current screen
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current_screen = None # Track the currently displayed screen so it can be replaced during navigation
        self.show_screen(HomeScreen) # Display the home screen when the app starts

    #----------------------------------------------------------------------------

    def setup_custom_theme(self): # Configure the app's colours, fonts and widget styles application-wide
        style = ttk.Style()
        custom_colours = { # Define the shared colour palette used throughout the application as a local variable
            'primary': "#3C3A46",
            'secondary': "#ACB2D7", # Modified after Beta Testing
            'success': "#61daae", 
            'info': '#A2B9CB',
            'warning': '#f6c23e',
            'danger': '#B3261E',
            'light': '#FFF6EB',
            'dark': '#5a5c69',
            'bg': "#7F8EC1", # Modified after Beta Testing
            'fg': '#2e2f37',
            'selectbg': '#eaecf4',
            'selectfg': "#ffffff",
            'border': '#A2B9CB',
            'inputfg': '#2e2f37',
            'inputbg': "#E2D9EF",
            'active': '#dddfeb'
            }
        
        # Use ttkbootstrap's Flatly theme as the base for the custom style
        style.theme_use('flatly')
        # Apply the custom colour palette to the base theme by overriding the colors in memory
        for color_name, hex_code in custom_colours.items():
            style.colors.set(color_name, hex_code)

        BG_COLOR = custom_colours['bg']

    #----------------------------------------------------------------------------

        # Main Heading
        style.configure('H1.TLabel', font=(HEADING_FONT, -48), foreground=custom_colours['primary'], 
                        background=BG_COLOR)
        # Question numbers
        style.configure('H2.TLabel', font=(BODY_FONT, -24), foreground=custom_colours['primary'], 
                        background=custom_colours['secondary'])
        # Menu subheadings and question text
        style.configure('H3.TLabel', font=(BODY_FONT, -18), foreground=custom_colours['primary'], 
                        background=custom_colours['secondary'])
        # User inputs and main answer text
        style.configure('H4.TLabel', font=(BODY_FONT, -16), foreground=custom_colours['primary'], 
                        background=BG_COLOR)
        # Explanatory and answer text
        style.configure('H5.TLabel', font=(BODY_FONT, -14), foreground=custom_colours['primary'], 
                        background=BG_COLOR)
        # Button text
        style.configure('H6.TButton', font=(BODY_FONT, -16), foreground=style.colors.light, 
                        background=style.colors.primary, bordercolor=style.colors.border, 
                        focuscolor=style.colors.border)
        style.map('H6.TButton', foreground=[('active', style.colors.light)], background=[('active', style.colors.info)])

        # Question header
        style.configure('H2-2.TLabel', font=(HEADING_FONT, -24), foreground=custom_colours['primary'], 
                        background=BG_COLOR)

    #----------------------------------------------------------------------------

        # Home screen specific fonts
        style.configure('HS2.TLabel', font=(HEADING_FONT, -20), foreground=custom_colours['primary'], 
                        background=custom_colours['secondary'])
        style.configure('HS4.TLabel', font=(BODY_FONT, -16), foreground=custom_colours['primary'], 
                        background=custom_colours['secondary'])
        style.configure('HS5.TLabel', font=(HEADING_FONT, -14), foreground=custom_colours['primary'], 
                        background=custom_colours['secondary'])

    #----------------------------------------------------------------------------
        # Combobox text
        style.configure('H4.TCombobox', font=(BODY_FONT, -16))

        #  Override widget states so the custom colour scheme remains visible when a combobox is read-only or disabled
        style.map('H4.TCombobox',
            fieldbackground=[('readonly', custom_colours['light']), ('disabled', custom_colours['light'])],
            foreground=[('readonly', custom_colours['fg']), ('disabled', custom_colours['fg'])],
            selectbackground=[('readonly', custom_colours['light'])], 
            selectforeground=[('readonly', custom_colours['fg'])])
        # Override dropdown colour and font to math the theme
        self.option_add('*TCombobox*Listbox.font', (BODY_FONT, -16))

        def on_dropdown_popdown(event): # Manually force the underlying combobox dropdown to accept custom colours 
            popdown = event.widget.tk.call('ttk::combobox::PopdownWindow', event.widget) 
            listbox = popdown + '.f.l'
            # Directly configure the underlying Tk graphic properties
            event.widget.tk.call(listbox, 'configure', '-background', custom_colours['light']) # Background color of the open dropdown menu list
            event.widget.tk.call(listbox, 'configure', '-foreground', custom_colours['primary']) # Text color of the unselected options inside the dropdown menu list
            event.widget.tk.call(listbox, 'configure', '-selectbackground', custom_colours['secondary']) # Highlight background color when you hover or arrow key down over an item
            event.widget.tk.call(listbox, 'configure', '-selectforeground', custom_colours['primary']) # Text color of the currently highlighted/selected option item
        self.bind_class('TCombobox', '<Map>', on_dropdown_popdown)  

    #---------------------------------------------------------------------------

        style.configure("Card.TFrame", background=style.colors.secondary, borderwidth=1, relief="solid")

    #---------------------------------------------------------------------------
        
        # Configure the notebook and the orientation of the bottom of the notebook
        style.configure('bottomtab.TNotebook', 
                        background=custom_colours['bg'], 
                        tabposition='s',
                        borderwidth=0,
                        highlightthickness=0,
                        lightcolor=custom_colours['bg'],
                        darkcolor=custom_colours['bg'],
                        bordercolor=custom_colours['bg']
                        )
        
        style.layout('bottomtab.TNotebook.Tab', [
            ('Notebook.tab', {'sticky': 'nswe', 'children': [
                ('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [
                    ('Notebook.label', {'side': 'top', 'sticky': ''})
                ]})
            ]})
        ])
        
        # Style the notebook tabs to be displayed below the analysis images
        style.configure('bottomtab.TNotebook.Tab', 
                        background=custom_colours['secondary'], 
                        foreground=custom_colours['primary'], 
                        padding=[15, 6], 
                        font=(BODY_FONT, 10, 'bold'),
                        borderwidth=0,
                        focuscolor=custom_colours['bg'],
                        bordercolor=custom_colours['bg'])
        
        # Maintain the custom colours for selected, active and focused tabs
        style.map('bottomtab.TNotebook.Tab', 
                    background=[
                    ('selected', custom_colours['primary']), 
                    ('active', custom_colours['active'])
                ], 
                foreground=[
                    ('selected', custom_colours['light']), 
                    ('active', custom_colours['fg'])
                ],
                bordercolor=[
                    ('selected', custom_colours['bg']),
                    ('active', custom_colours['bg']),
                    ('focus', custom_colours['bg'])
                ],
                lightcolor=[
                    ('selected', custom_colours['bg']),
                    ('focus', custom_colours['bg'])
                ],
                darkcolor=[
                    ('selected', custom_colours['bg']),
                    ('focus', custom_colours['bg'])
                ])

    #------------------------------------------------------------------------------

    def show_screen(self, screen_class): # Replace the current screen with a new screen object
        '''
    Parameters:
        screen_class (class) is the screen class to be displayed.
            - A class is passed so that 'App' can create the 'screen' object when navigation occurs.
        '''
        if self.current_screen is not None: # Remove the previous screen before displaying the new one.
            self.current_screen.destroy()
        self.current_screen = screen_class(self.container, self)
        self.current_screen.pack(fill="both", expand=True)
# Potential future development could replace this with seperate functions for each screen

    #----------------------------------------------------------------------------

    def get_current_username(self): # Return the current username, or 'None' for a guest
        return self.current_user

    #----------------------------------------------------------------------------

