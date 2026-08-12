from app import App

def main(): # Create the application object and start the GUI event loop
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

# NOTES -> move username storage to app class cause screen classes should just be navigation and layout !!!