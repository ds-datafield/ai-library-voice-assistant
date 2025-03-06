import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager

# Define a Book dataclass to represent a book in the library
@dataclass
class Book:
    title: str  # Title of the book
    author: str  # Author of the book
    genre: str  # Genre of the book
    available: bool  # True if the book is available, False if it's reserved

# Define the DatabaseLibrary class to handle database operations
class DatabaseLibrary:
    def __init__(self, db_path: str = "library_db.sqlite"):
        """
        Initialize the database connection and set up the database if it doesn't exist.
        """
        self.db_path = db_path # Path to the SQLite database file
        self._init_db()  # Initialize the database

    @contextmanager
    def _get_connection(self):
        """
        A context manager to handle database connections.
        It ensures the connection is properly closed after use.
        """
        conn = sqlite3.connect(self.db_path) # Connect to the SQLite database
        try:
            yield conn # Yield the connection for use in the with block.
            #When the with block is entered, the code runs up to the yield statement and yields the connection object (conn) to the with block.
            # The with block can then use the connection to perform database operations.
        finally:
            #The finally block ensures that the connection is always closed, even if an exception occurs inside the with block.
            conn.close() # Close the connection when done.

    def _init_db(self):
        """
        Initialize the database by creating the books table if it doesn't already exist.
        """
        with self._get_connection() as conn:#Here, conn is the connection object yielded by _get_connection.
            cursor = conn.cursor()
            
            # Create the books table with columns: title, author, genre, available
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT PRIMARY KEY,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    available BOOLEAN NOT NULL
                )
            """)
            conn.commit() # Commit the changes to the database

    def create_book(self, title: str, author: str, genre: str, available: bool = True) -> Book:
        """
        Add a new book to the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Insert the book into the books table
                cursor.execute(
                    "INSERT INTO books (title, author, genre, available) VALUES (?, ?, ?, ?)",
                    (title, author, genre, available)
                )
                conn.commit()# Commit the changes to the database
                return Book(title=title, author=author,genre=genre, available=available)
            except sqlite3.IntegrityError:
                # Handle the case where the book already exists in the database
                print(f"⚠️ Book '{title}' already exists in the database. Skipping...")
                return None


    def get_book_by_title(self, title: str) -> Optional[Book]:
        """
        Retrieve a book from the database by its title.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Perform a case-insensitive search for the book as we don't always know how TTS and STT perform
            cursor.execute("SELECT * FROM books WHERE LOWER(title) = LOWER(?)", (title.strip().lower(),))
            row = cursor.fetchone()# Fetch the first matching row
            if not row:
                return None # Return None if no book is found
            
            # Return a Book object with the retrieved data
            return Book(
                title=row[0],
                author=row[1],
                genre=row[2],  
                available=row[3]
            )
    def get_books_by_genre(self, genre: str) -> List[Book]:
        """
        Retrieve all books in a specific genre from the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
             # Perform a case-insensitive search for the book as we don't always know how TTS and STT perform
            cursor.execute("SELECT * FROM books WHERE LOWER(genre) = LOWER(?)", (genre.strip().lower(),))
            rows = cursor.fetchall()# Fetch the first matching row
            
            # Return a list of Book objects
            return [
                Book(title=row[0], author=row[1], genre=row[2], available=row[3])
                for row in rows
            ]
        
    def reserve_book(self, title: str) -> str:
        """
        Reserve a book if it is available.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if the book exists and is available
            cursor.execute("SELECT available FROM books WHERE LOWER(title) = LOWER(?)", (title.strip().lower(),))
            row = cursor.fetchone()

            if not row:
                return f"❌ Book '{title}' not found in the database."

            if not row[0]:  # If book is already reserved
                return f"⛔ Sorry, the book '{title}' is already reserved."

            # Reserve the book by setting available to FALSE
            cursor.execute("UPDATE books SET available = FALSE WHERE LOWER(title) = LOWER(?)", (title.strip().lower(),))
            conn.commit()
            return f"📖 Book '{title}' has been successfully reserved and is no longer available!"



    def return_book(self, title: str) -> str:
        """
        Return a book to the library, marking it as available.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if the book exists
            cursor.execute("SELECT available FROM books WHERE LOWER(title) = LOWER(?)", (title.strip().lower(),))
            row = cursor.fetchone()
            print("row is: ",row)
            
            if not row:
                return f"❌ Book '{title}' not found in the database."
            
            if row[0]:  # If book is already available
                return f"✅ Book '{title}' is already available."

            # Mark the book as available again
            cursor.execute("UPDATE books SET available = 1 WHERE LOWER(title) = LOWER(?)", (title.strip().lower(),))
            conn.commit()
            return f"📚 Book '{title}' has been returned successfully."
        

    def get_available_books(self) -> List[Book]:
        """
        Retrieve all available books from the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Fetch all books where available is TRUE
            cursor.execute("SELECT * FROM books WHERE available = TRUE")
            rows = cursor.fetchall()
            # Return a list of Book objects
            return [
                Book(title=row[0], author=row[1], genre=row[2], available=row[3])
                for row in rows
            ]
        
    def get_non_available_books(self) -> List[Book]:
        """
        Retrieve all reserved books from the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Fetch all books where available is FALSE
            cursor.execute("SELECT * FROM books WHERE available = FALSE")
            rows = cursor.fetchall()

            # Return a list of Book objects
            return [
                Book(title=row[0], author=row[1], genre=row[2], available=row[3])
                for row in rows
            ]