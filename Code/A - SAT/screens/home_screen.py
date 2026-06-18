from tkinter import * # idk what this part does
from ttkbootstrap.constants import * # idk what this part does either
import ttkbootstrap as ttk

root = ttk.Window(themename="superhero") # uses a default pre-determined theme 

#root = Tk()
root.title("Home Screen")
#root.iconbitmap('images/codemy.ico') also not sure what this bit does (referencing freeCodeCamp.org youtube tutorial...)
root.geometry('1366x768') #The screen size matches that of the Chromebook itself

# create a function for the button (should be moved to a different folder?)

# create a label
label_try = ttk.Label(text="Test!", font=("Roboto", 16), bootstyle="default")
label_try.pack(pady=50) #15 minutes into video...


root.mainloop()