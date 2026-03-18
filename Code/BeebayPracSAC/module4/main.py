from app import App


def main(): #internal loop
    app = App() #creates an instance of the "App" class and automatically calls the constructor
    app.run() #run is a method because it's part of a class


if __name__ == "__main__":
    main() #main is a function
