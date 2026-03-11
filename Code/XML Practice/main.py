from models.book import Book
from repos.bookRepoXml import BookRepoXml

from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    xml_path = data_dir / "books.xml"
    
    repo = BookRepoXml(xml_path)
    # Load existing data
    books = repo.load()

    print("Current books")
    print("-------------------")

    for book in books:
        print(f"{book.title}, {book.author}, {book.price}") #ask about how to add a $ sign
    
    print()

    # Example CRUD update
    title_to_update = input("Enter book title to update: ")
    
    for book in books:
        if book.title.lower() == title_to_update.lower():
            new_price = input("Enter new price: ")
            book.price = new_price
            print("Price updated.")
            break
    else:
        print("Book not found.")
    
    # Save changes
    repo.save(books)
    
    print("Data saved.")


if __name__ == "__main__":
    main()