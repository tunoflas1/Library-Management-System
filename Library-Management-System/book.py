import csv
import os


class Book:
    """It represents a book in the library."""

    def __init__(self, id, title, author, genre):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = True

    def show(self):
        """It prints the book information to the screen."""
        status = "available" if self.available else "borrowed"
        print(f"  [{self.id}] {self.title} by {self.author} - {self.genre} - {status}")

    def toggle_available(self):
        """It changes the current/loan status of the book."""
        self.available = not self.available

    def update_genre(self, new_genre):
        """It updates the book's genre."""
        self.genre = new_genre
        print(f"Genre updated to {self.genre}.")

    def update_author(self, new_author):
        """It updates the author of the book."""
        self.author = new_author
        print(f"Author updated to {self.author}.")

    def __str__(self):
        """returns the book in written form."""
        return f"{self.title} ({self.author})"


class BookCatalog:
    """manages all the books in the library."""

    def __init__(self):
        self.books = []
        self.next_id = 1

    def add(self, title, author, genre):
        """It adds new books to the catalog."""
        b = Book(self.next_id, title, author, genre)
        self.books.append(b)
        self.next_id += 1
        print(f"'{title}' added to catalog.")
        return b

    def find(self, id):
        """It searches for books based on their ID, and returns None if it doesn't find any."""
        for b in self.books:
            if b.id == id:
                return b
        return None

    def search(self, keyword):
        """It searches for books by title or author."""
        results = []
        for b in self.books:
            if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower():
                results.append(b)
        return results

    def show_all(self):
        """It lists all the books."""
        if len(self.books) == 0:
            print("No books in catalog.")
            return
        print("\nAll books:")
        for b in self.books:
            b.show()

    def show_available(self):
        """It only lists available books."""
        found = False
        print("\nAvailable books:")
        for b in self.books:
            if b.available:
                b.show()
                found = True
        if not found:
            print("  No available books right now.")

    def save_csv(self, path="data/books.csv"):
        """The book saves the data to a CSV file."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "title", "author", "genre", "available"])
                for b in self.books:
                    w.writerow([b.id, b.title, b.author, b.genre, b.available])
            print("Books saved.")
        except Exception as e:
            print(f"Error: {e}")

    def load_csv(self, path="data/books.csv"):
        """The book loads data from a CSV file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                r = csv.DictReader(f)
                self.books = []
                for row in r:
                    b = Book(int(row["id"]), row["title"], row["author"], row["genre"])
                    b.available = row["available"] == "True"
                    self.books.append(b)
                if len(self.books) > 0:
                    self.next_id = max(b.id for b in self.books) + 1
            print(f"Books loaded. {len(self.books)} found.")
        except FileNotFoundError:
            print(f"{path} not found. Starting empty.")
        except Exception as e:
            print(f"Error: {e}")
