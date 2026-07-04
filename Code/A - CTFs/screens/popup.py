import ttkbootstrap as ttk


class ResultPopup(ttk.Toplevel):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)

        # ----- Window -----
        self.title(title)
        self.geometry("420x220")
        self.resizable(False, False)

        # Makes it behave like a popup
        self.transient(parent)
        self.grab_set()

        # ----- Main frame -----
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)

        # ----- Heading -----
        ttk.Label(
            frame,
            text=title,
            style="H2.TLabel"
        ).pack(pady=(0, 15))

        # ----- Message -----
        ttk.Label(
            frame,
            text=message,
            style="H4.TLabel",
            justify="center",
            wraplength=340
        ).pack()

        # ----- Button -----
        ttk.Button(
            frame,
            text=button_text,
            style="H6.TButton",
            command=self.destroy
        ).pack(pady=25)

        # Centre over parent
        self.update_idletasks()

        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (420 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (220 // 2)

        self.geometry(f"+{x}+{y}")