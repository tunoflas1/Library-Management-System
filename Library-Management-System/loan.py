import csv
import os
from datetime import datetime, timedelta


class Loan:
    """It represents a loan record."""

    def __init__(self, id, member, book):
        self.id = id
        self.member = member
        self.book = book
        self.borrow_date = datetime.now()
        self.due_date = datetime.now() + timedelta(days=14)
        self.returned = False

    def show(self):
        """It prints the loan record to the screen."""
        status = "Returned" if self.returned else "Active"
        print(f"\nLoan #{self.id}")
        print(f"  Member  : {self.member.name}")
        print(f"  Book    : {self.book.title}")
        print(f"  Borrowed: {self.borrow_date.strftime('%d/%m/%Y')}")
        print(f"  Due     : {self.due_date.strftime('%d/%m/%Y')}")
        print(f"  Status  : {status}")

    def return_book(self):
        """They return the book and update the relevant records."""
        if self.returned:
            print("This book was already returned.")
            return False
        self.returned = True
        self.book.toggle_available()
        self.member.loan_count -= 1
        print(f"'{self.book.title}' returned by {self.member.name}.")
        return True

    def is_overdue(self):
        """It checks if the loan has expired."""
        if not self.returned and datetime.now() > self.due_date:
            return True
        return False

    def days_left(self):
        """Returns the number of days remaining."""
        if self.returned:
            return 0
        diff = self.due_date - datetime.now()
        return diff.days

    def __str__(self):
        """It returns the loan record as text."""
        return f"Loan #{self.id}: {self.book.title} -> {self.member.name}"


class LoanManager:
    """It manages all loan records."""

    def __init__(self):
        self.loans = []
        self.next_id = 1

    def create(self, member, book):
        """It creates a new loan record."""
        if not book.available:
            print(f"'{book.title}' is not available right now.")
            return None
        loan = Loan(self.next_id, member, book)
        self.loans.append(loan)
        self.next_id += 1
        book.toggle_available()
        member.loan_count += 1
        print(f"Loan #{loan.id} created. Due: {loan.due_date.strftime('%d/%m/%Y')}")
        return loan

    def find(self, id):
        """It searches for loan records based on the ID, and returns None if it doesn't find any."""
        for l in self.loans:
            if l.id == id:
                return l
        return None

    def show_active(self):
        """It lists unreturned loan records."""
        found = False
        print("\nActive loans:")
        for l in self.loans:
            if not l.returned:
                overdue = " [OVERDUE]" if l.is_overdue() else f" ({l.days_left()} days left)"
                print(f"  [{l.id}] {l.book.title} - {l.member.name}{overdue}")
                found = True
        if not found:
            print("  No active loans.")

    def show_overdue(self):
        """It lists overdue loans."""
        found = False
        print("\nOverdue loans:")
        for l in self.loans:
            if l.is_overdue():
                print(f"  [{l.id}] {l.book.title} - {l.member.name}")
                found = True
        if not found:
            print("  No overdue loans.")

    def save_csv(self, path="data/loans.csv"):
        """It saves loan records to a CSV file."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "member", "book", "borrow_date", "due_date", "returned"])
                for l in self.loans:
                    w.writerow([
                        l.id,
                        l.member.name,
                        l.book.title,
                        l.borrow_date.strftime("%d/%m/%Y"),
                        l.due_date.strftime("%d/%m/%Y"),
                        l.returned
                    ])
            print("Loans saved.")
        except Exception as e:
            print(f"Error: {e}")
