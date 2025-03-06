import logging
from livekit.agents import llm
import enum
from typing import Annotated
from db_library import DatabaseLibrary


# Set up a logger for the library data operations
logger = logging.getLogger("library-data")
logger.setLevel(logging.INFO)

# Initialize the database connection
DB = DatabaseLibrary()

# Define what are the book details (title, author, genre, availability).
# Note: Availability will be change in the future for number of copy of a book
class BookDetails(enum.Enum):
    TITLE = "title"
    AUTHOR = "author"
    GENRE = "genre"
    AVAILABLE = "available"


# Define the AssistantFnc class, which extends llm.FunctionContext
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()

        self.first_connection = True  # Flag to track first interaction
        
        # Dictionary to store details of the currently queried book
        self._book_details = {
            BookDetails.TITLE: "",
            BookDetails.AUTHOR: "",
            BookDetails.GENRE: "",
            BookDetails.AVAILABLE: False
        }

    def on_session_start(self, session):
        """ Trigger a greeting message when a new session starts.
            This method is called when the user first interacts with the assistant.
        """
        if self.first_connection:
            logger.info("First connection detected. Sending greeting message.")
            session.conversation.item.create(
                llm.ChatMessage(
                    role="assistant",
                    content="Hello, I'm the Library AI Assistant. How can I help you today?"
                )
            )
            session.response.create()
            # Ensure the greeting is only sent once per session
            self.first_connection = False 


    def get_book_str(self):
        """
        Format the book details into a readable string.
        """
        return f"Title: {self._book_details[BookDetails.TITLE]}\nAuthor: {self._book_details[BookDetails.AUTHOR]}\nGenre: {self._book_details[BookDetails.GENRE]}\nAvailable: {'Yes' if self._book_details[BookDetails.AVAILABLE] else 'No'}"



    @llm.ai_callable(description="Lookup a book by its title")

    def lookup_book(self, title: Annotated[str, llm.TypeInfo(description="The title of the book to lookup")]):
        """
        Look up a book by its title in the database and return its details.
        """

        logger.info(f"Looking up book: {title}")

        # Query the database for the book
        result = DB.get_book_by_title(title)
        logger.info(f"DB Lookup Result: {result}") 

        # If the book is not found, return a message
        if result is None:
            return f"Sorry, the book '{title}' is not found in our library."

        # Update the book details in the assistant's state
        self._book_details = {
            BookDetails.TITLE: result.title,
            BookDetails.AUTHOR: result.author,
            BookDetails.GENRE: result.genre,
            BookDetails.AVAILABLE: result.available
        }

        # Return the formatted book details       
        return f"The book details are:\n{self.get_book_str()}"



    @llm.ai_callable(description="Check if a book is available")
    def check_book_availability(self, title: str):
        """
        Check if a book is available in the library.
        """
        logger.info("Waiting for user input...")

        # Validate the input title
        if not title:
            return "Please specify the book title."
        
        # Query the database for the book
        result = DB.get_book_by_title(title)
        if result is None:
            return f"The book '{title}' is not in our library database."

        # Return the availability status
        return f"The book '{title}' is {'available' if result.available else 'currently reserved'}."



    @llm.ai_callable(description="Reserve a book if available")
    def reserve_book(self, title: str):
        """
        Reserve a book if it is available.
        """
        logger.info("Waiting for user input...")


        # Validate the input title
        if not title:
            return "Please specify the book title."
        
        # Query the database for the book
        result = DB.get_book_by_title(title)
        if result is None:
            return f"The book '{title}' is not found in our system."
        
        # Check if the book is already reserved
        if not result.available:
            return f"Sorry, the book '{title}' is already reserved."

        # Reserve the book
        DB.reserve_book(title)
        return f"The book '{title}' has been successfully reserved for you!"



    @llm.ai_callable(description="Recommend available books by genre")
    def recommend_books_by_genre(self, genre: str):
        """
        Recommend available books in a specific genre.
        """
        logger.info("Waiting for user input...")

        # Validate the input genre
        if not genre:
            return "Please specify a genre for the recommendation."

        logger.info(f"Searching for available books in the genre: {genre}")

        # Query the database for books in the specified genre
        books = DB.get_books_by_genre(genre)

        # Filter only available books
        available_books = [book for book in books if book.available]

        if not available_books:
            return f"Sorry, there are no available books in the '{genre}' genre at the moment."
       
        # Format the recommendations into a readable string
        recommendations = "\n".join(f"- {book.title} by {book.author}" for book in available_books)
        return f"Here are some available {genre} books:\n{recommendations}"

    def has_book(self):
        """
        Check if the assistant currently has a book in its state.
        The method checks whether the assistant currently has a book 
        in its state by verifying if the title field in self._book_details is not empty.
        """
        return self._book_details[BookDetails.TITLE] != ""



    @llm.ai_callable(description='Returning a book')
    def returning_book(self, title: str):
        """
        Return a book to the library.
        """
        logger.info("Waiting for user input...")

        # Validate the input title
        if not title:
            return "Please specify the book title."
        
        # Try to return the book by his title
        result = DB.return_book(title)
        if result is None:
            return f"The book '{title}' couldn't be returned."
        return f"The book '{title}' has been successfully returned."
