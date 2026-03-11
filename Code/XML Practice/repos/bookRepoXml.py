from pathlib import Path
import xml.etree.ElementTree as ET
from models.book import Book
#repo controls the data! aka takes it out and puts it in

class BookRepoXml:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        root = ET.parse(Path(self.file_path)).getroot()
        books: list[Book] = []
        
        for book_el in root.findall("book"):
            title = book_el.findtext("title").strip()
            author = book_el.findtext("author").strip()
            price = book_el.findtext("price").strip()
            
            books.append(
                Book(title = title, author=author, price=price)
            )
        
        return books

    def save(self, books):
        root = ET.Element("books")
        
        for book in books:
            book_el = ET.SubElement(root, "book")
            
            title_el = ET.SubElement(book_el, "title")
            title_el.text = book.title
            
            author_el = ET.SubElement(book_el, "author")
            author_el.text = book.author
            
            price_el = ET.SubElement(book_el, "price")
            price_el.text = book.price
        
        ET.indent(root)
        
        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)