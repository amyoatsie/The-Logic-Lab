from app import App

def main(): # Create the application object and start the GUI event loop
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

# NOTHING more needs to be added to this section
# NOTES -> could add a notebook section for notes which is written & read to a csv throughout each OUT OF SCOPE
# NOTES -> move username storage to app class cause screen classes should just be navigation and layout !!!
# NOTES -> if a 'guest' user gets all 4 right, show a message that says 'sign in to save progress/continue' DONE
# NOTES -> convert username to all caps/all lower NVM DONE