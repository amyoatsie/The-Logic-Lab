from tkinter import * # imports all of tkinter?
from ttkbootstrap.constants import * # type: ignore # This imports constants like LEFT, RIGHT, TOP, BOTTOM
import ttkbootstrap as ttk # type: ignore CHANGE SCREEN NAME LMAO

class homeScreen(ttk.Frame): # Inherit from ttk.Frame so this file acts as a modular screen page
    def __init__(self, parent):
        super().__init__(parent) # Initialize the frame inside the parent container (app.py)
        