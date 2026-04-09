import csv
import os


class Member:
    """It represents the library member."""

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.loan_count = 0

    def show(self):
        """It prints member information to the screen."""
        print(f"\n  ID     : {self.id}")
        print(f"  Name   : {self.name}")
        print(f"  Email  : {self.email}")
        print(f"  Loans  : {self.loan_count}")

    def update_email(self, new_email):
        """Updates the member's email address."""
        self.email = new_email
        print(f"{self.name} email updated.")

    def update_name(self, new_name):
        """Updates the member's name."""
        self.name = new_name
        print(f"Name updated to {self.name}.")

    def is_active(self):
        """It checks whether the member has an active loan."""
        if self.loan_count > 0:
            return True
        return False

    def __str__(self):
        """It returns the member as text."""
        return f"{self.name} (ID: {self.id})"


class MemberManager:
    """It manages all library members."""

    def __init__(self):
        self.members = []
        self.next_id = 1

    def add(self, name, email):
        """Adds new members."""
        m = Member(self.next_id, name, email)
        self.members.append(m)
        self.next_id += 1
        print(f"{name} registered as member.")
        return m

    def find(self, id):
        """It searches for members based on their ID, and returns None if no members are found."""
        for m in self.members:
            if m.id == id:
                return m
        return None

    def show_all(self):
        """It lists all members."""
        if len(self.members) == 0:
            print("No members yet.")
            return
        print("\nMembers:")
        for m in self.members:
            active = " [has loans]" if m.is_active() else ""
            print(f"  [{m.id}] {m.name} - {m.email}{active}")

    def show_active(self):
        """It lists members who are active lenders."""
        found = False
        print("\nMembers with active loans:")
        for m in self.members:
            if m.is_active():
                print(f"  {m.name} - {m.loan_count} loan(s)")
                found = True
        if not found:
            print("  No active loans.")

    def save_csv(self, path="data/members.csv"):
        """It saves member data to a CSV file."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "name", "email", "loan_count"])
                for m in self.members:
                    w.writerow([m.id, m.name, m.email, m.loan_count])
            print("Members saved.")
        except Exception as e:
            print(f"Error: {e}")

    def load_csv(self, path="data/members.csv"):
        """The member uploads their data from a CSV file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                r = csv.DictReader(f)
                self.members = []
                for row in r:
                    m = Member(int(row["id"]), row["name"], row["email"])
                    m.loan_count = int(row["loan_count"])
                    self.members.append(m)
                if len(self.members) > 0:
                    self.next_id = max(m.id for m in self.members) + 1
            print(f"Members loaded. {len(self.members)} found.")
        except FileNotFoundError:
            print(f"{path} not found. Starting empty.")
        except Exception as e:
            print(f"Error: {e}")
