import ttkbootstrap as ttk

class ResultPopup(ttk.Toplevel):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        #button_text="OK" shoulf be a parameter???

        # Makes it behave like a popup
        self.transient(parent)
        self.grab_set()

        ttk.Label(frame, text=title, style="H2-2.TLabel").pack(pady=(0, 15))
        ttk.Label(frame, text=message, style="H4.TLabel", justify="center", wraplength=340).pack() # center or centre???

        button = ttk.Button(frame, text=button_text, style="H6.TButton", command=self.destroy)
        button.place(x=75, y=110, width=200, height=45)

        # Centre over  (math!)
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (420 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (220 // 2)
        self.geometry(f"+{x}+{y}")