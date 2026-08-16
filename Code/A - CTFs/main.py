from app import App

def main(): # Create the application object and start the GUI event loop
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

# NOTES -> move username storage to app class cause screen classes should just be navigation and layout !!!
# add ''''' before EACH class and function (not really inside, only if complicated, unusual, or ur proud of it)
# each thing passed in should be defined as what type, and why it is that type (not the end of the world tho)