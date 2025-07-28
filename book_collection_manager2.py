import psycopg2
from psycopg2 import Error
from datetime import datetime
import csv
import json

class DatabaseConnection:
    def __init__(self):
        self.db_params = {
            'dbname': 'book_collection',
            'user': 'postgres',
            'password': 'Ch!maera1313',
            'host': 'localhost',
            'port': '5432'
        }

    def get_connection(self):
        return psycopg2.connect(**self.db_params)

class BookDatabase:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def get_genres(self):
        """Get all available genres"""
        query = "SELECT id, name FROM genres ORDER BY name;"
        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving genres: {e}")
            return []

    def add_book(self, title, author, year, isbn=None, description=None, copies=1, genre_ids=None):
        """Add a new book to the database"""
        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insert book
                    query = """
                        INSERT INTO books (title, author, year, isbn, description, 
                                         total_copies, available_copies)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """
                    cursor.execute(query, (title, author, year, isbn, description, 
                                         copies, copies))
                    book_id = cursor.fetchone()[0]

                    # Add genres
                    if genre_ids:
                        genre_query = """
                            INSERT INTO books_genres (book_id, genre_id)
                            VALUES (%s, %s);
                        """
                        for genre_id in genre_ids:
                            cursor.execute(genre_query, (book_id, genre_id))

                    return book_id
        except Error as e:
            print(f"Error adding book: {e}")
            return None

    def get_all_books(self):
        """Retrieve all books with their genres"""
        query = """
            SELECT b.id, b.title, b.author, b.year, b.isbn, b.description,
                   b.total_copies, b.available_copies, b.date_added,
                   string_agg(g.name, ', ') as genres
            FROM books b
            LEFT JOIN books_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            GROUP BY b.id
            ORDER BY b.title;
        """
        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving books: {e}")
            return []

    def export_to_csv(self, filename):
        """Export the book collection to CSV"""
        books = self.get_all_books()
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Author', 'Year', 'ISBN', 
                               'Description', 'Total Copies', 'Available Copies',
                               'Date Added', 'Genres'])
                for book in books:
                    writer.writerow(book)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def export_to_json(self, filename):
        """Export the book collection to JSON"""
        books = self.get_all_books()
        try:
            book_list = []
            for book in books:
                book_dict = {
                    'id': book[0],
                    'title': book[1],
                    'author': book[2],
                    'year': book[3],
                    'isbn': book[4],
                    'description': book[5],
                    'total_copies': book[6],
                    'available_copies': book[7],
                    'date_added': book[8].strftime('%Y-%m-%d %H:%M:%S'),
                    'genres': book[9].split(', ') if book[9] else []
                }
                book_list.append(book_dict)

            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(book_list, file, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

class BookCollectionManager:
    def __init__(self):
        self.db = BookDatabase()

    def display_menu(self):
        print("\nBook Collection Manager")
        print("1. Add a book")
        print("2. Display all books")
        print("3. Search books")
        print("4. Delete a book")
        print("5. Export collection")
        print("6. Exit")

    def display_genres(self):
        genres = self.db.get_genres()
        print("\nAvailable Genres:")
        for genre_id, genre_name in genres:
            print(f"{genre_id}: {genre_name}")
        return genres

    def add_book(self):
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        
        while True:
            try:
                year = int(input("Enter publication year: "))
                if 0 <= year <= datetime.now().year:
                    break
                print(f"Please enter a valid year (0-{datetime.now().year})")
            except ValueError:
                print("Please enter a valid number for the year")
        
        isbn = input("Enter ISBN (optional, press Enter to skip): ").strip() or None
        description = input("Enter book description (optional, press Enter to skip): ").strip() or None
        
        while True:
            try:
                copies = int(input("Enter number of copies: "))
                if copies > 0:
                    break
                print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")

        genres = self.display_genres()
        genre_ids = []
        while True:
            genre_input = input("\nEnter genre IDs (comma-separated) or press Enter to skip: ").strip()
            if not genre_input:
                break
            try:
                genre_ids = [int(g.strip()) for g in genre_input.split(',')]
                if all(any(g[0] == gid for g in genres) for gid in genre_ids):
                    break
                print("Please enter valid genre IDs")
            except ValueError:
                print("Please enter valid numbers")

        book_id = self.db.add_book(title, author, year, isbn, description, copies, genre_ids)
        if book_id:
            print(f"\nBook added successfully with ID: {book_id}")
        else:
            print("\nFailed to add book")

    def display_books(self, books):
        if not books:
            print("\nNo books found.")
            return

        print("\nBook Collection:")
        print("-" * 120)
        print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Year':<6} {'Copies':<12} {'Genres':<20} {'Description':<30}")
        print("-" * 120)
        for book in books:
            description = (book[5][:27] + '...') if book[5] and len(book[5]) > 30 else (book[5] or 'N/A')
            copies = f"{book[7]}/{book[6]}"
            genres = book[9] if book[9] else 'N/A'
            print(f"{book[0]:<5} {book[1][:25]:<25} {book[2][:20]:<20} {book[3]:<6} "
                  f"{copies:<12} {genres[:20]:<20} {description:<30}")

    def export_collection(self):
        print("\nExport Collection")
        print("1. Export to CSV")
        print("2. Export to JSON")
        print("3. Cancel")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice in ['1', '2']:
            filename = input("Enter filename (without extension): ").strip()
            if choice == '1':
                filename = f"{filename}.csv"
                if self.db.export_to_csv(filename):
                    print(f"\nCollection exported to {filename}")
                else:
                    print("\nExport failed")
            else:
                filename = f"{filename}.json"
                if self.db.export_to_json(filename):
                    print(f"\nCollection exported to {filename}")
                else:
                    print("\nExport failed")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.display_books(self.db.get_all_books())
            elif choice == '3':
                self.search_books()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                self.export_collection()
            elif choice == '6':
                print("\nThank you for using Book Collection Manager!")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    manager = BookCollectionManager()
    manager.run()
