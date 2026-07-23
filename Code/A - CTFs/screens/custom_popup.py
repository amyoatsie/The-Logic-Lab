import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ResultPopup(ttk.Toplevel):
    def __init__(self, parent, title, message, button_text="OK", show_input=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)

        # Makes it behave like a popup
        self.transient(parent)
        self.grab_set()

        self.user_input_value = None

        ttk.Label(frame, text=title, style="H2-2.TLabel").pack(pady=(0, 15))
        ttk.Label(frame, text=message, style="H4.TLabel", justify="center", wraplength=340).pack() # center or centre???

        # Conditional input field for username authentication
        if show_input:
            self.entry_var = ttk.StringVar()
            self.entry_field = ttk.Entry(frame, textvariable=self.entry_var, font=("Helvetica", 12))
            self.entry_field.pack(fill=X, padx=20, pady=(0, 15))
            self.entry_field.focus_set()
            
            # Pressing enter submits the prompt automatically (for ease of use)
            self.entry_field.bind("<Return>", lambda e: self.on_submit())
            button_cmd = self.on_submit
        else:
            button_cmd = self.destroy

        button = ttk.Button(frame, text=button_text, style="H6.TButton", command=button_cmd)
        button.place(x=75, y=120, width=200, height=45)

        # Centre the popup
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (420 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (220 // 2)
        self.geometry(f"+{x}+{y}")

        self.wait_window()

    #----------------------------------------------------------------------------

    def on_submit(self): # Save entry information before closing
        self.user_input_value = self.entry_var.get().strip()
        self.destroy()