from app import App #WILL ALWAYS LOOK LIKE THIS


def main(): #internal loop
    app = App() #creates an instance of the "app" class
    app.run()


if __name__ == "__main__":
    main()

#ToDo: add type validation in inputs
#Error - When altered information and haven't clicked calculate, csv updates with old "total" information