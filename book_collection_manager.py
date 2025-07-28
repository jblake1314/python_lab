class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"


class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, year):
        book = Book(title, author, year)
        self.books.append(book)
        print(f"Added: {book}")

    def display_books(self):
        if not self.books:
            print("No books in the collection.")
            return
        
        print("\nBook Collection:")
        print("-" * 40)
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

    def search_by_title(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        if found_books:
            print(f"\nFound {len(found_books)} book(s) with title '{title}':")
            for book in found_books:
                print(book)
        else:
            print(f"No books found with title '{title}'")

    def remove_book(self, index):
        if 1 <= index <= len(self.books):
            removed_book = self.books.pop(index - 1)
            print(f"Removed: {removed_book}")
        else:
            print("Invalid book index")


def main():
    collection = BookCollection()
    
    while True:
        print("\nBook Collection Manager")
        print("1. Add a book")
        print("2. Display all books")
        print("3. Search by title")
        print("4. Remove a book")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            year = input("Enter publication year: ")
            try:
                year = int(year)
                collection.add_book(title, author, year)
            except ValueError:
                print("Invalid year! Please enter a valid number.")
                
        elif choice == '2':
            collection.display_books()
            
        elif choice == '3':
            title = input("Enter title to search: ")
            collection.search_by_title(title)
            
        elif choice == '4':
            collection.display_books()
            try:
                index = int(input("Enter the number of the book to remove: "))
                collection.remove_book(index)
            except ValueError:
                print("Invalid input! Please enter a number.")
                
        elif choice == '5':
            print("Thank you for using Book Collection Manager!")
            break
            
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
