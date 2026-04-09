from book import BookCatalog
from member import MemberManager
from loan import LoanManager


def load_data(catalog, mm):
    """It loads saved data from files."""
    catalog.load_csv()
    mm.load_csv()


def setup_sample_books(catalog):
    """If the catalog is empty, it adds sample books."""
    catalog.add("Ince Memed", "Yashar Kemal", "Roman")
    catalog.add("Sabahat", "Ahmet Hamdi Tanpinar", "Roman")
    catalog.add("Kuyucakli Yusuf", "Sabahattin Ali", "Roman")
    catalog.add("Tutunamayanlar", "Oguz Atay", "Roman")
    catalog.add("Sinekli Bakkal", "Halide Edib Adivar", "Tarihi Roman")
    catalog.add("Araba Sevdasi", "Recaizade Mahmut Ekrem", "Klasik")
    catalog.add("Serefsiz", "Emre Dorman", "Psikoloji")
    catalog.add("Istanbul'u Dinliyorum", "Orhan Veli Kanik", "Siir")


def book_management(catalog):
    """Launches the book management screen."""
    while True:
        print("\nBook Management:")
        print("1. Show all books")
        print("2. Show available books")
        print("3. Add new book")
        print("4. Search book")
        print("5. Update book genre")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            catalog.show_all()

        elif choice == "2":
            catalog.show_available()

        elif choice == "3":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            catalog.add(title, author, genre)
            catalog.save_csv()

        elif choice == "4":
            keyword = input("Search (title or author): ").strip()
            results = catalog.search(keyword)
            if len(results) == 0:
                print("No books found.")
            else:
                print(f"\n{len(results)} result(s):")
                for b in results:
                    b.show()

        elif choice == "5":
            catalog.show_all()
            try:
                id = int(input("Book ID: "))
                b = catalog.find(id)
                if b is None:
                    print("Book not found.")
                    continue
                new_genre = input("New genre: ").strip()
                b.update_genre(new_genre)
                catalog.save_csv()
            except ValueError:
                print("Invalid input.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def member_management(mm):
    """Launches the member management screen."""
    while True:
        print("\nMember Management:")
        print("1. List all members")
        print("2. Add new member")
        print("3. View member details")
        print("4. Members with active loans")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            mm.show_all()

        elif choice == "2":
            name = input("Name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            email = input("Email: ").strip()
            mm.add(name, email)
            mm.save_csv()

        elif choice == "3":
            mm.show_all()
            try:
                id = int(input("Member ID: "))
                m = mm.find(id)
                if m is None:
                    print("Member not found.")
                else:
                    m.show()
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            mm.show_active()

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def loan_management(catalog, mm, lm):
    """Launches the loan management screen."""
    while True:
        print("\nLoan Management:")
        print("1. Borrow a book")
        print("2. Return a book")
        print("3. Show active loans")
        print("4. Show overdue loans")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            catalog.show_available()
            mm.show_all()
            try:
                bid = int(input("Book ID: "))
                b = catalog.find(bid)
                if b is None:
                    print("Book not found.")
                    continue

                mid = int(input("Member ID: "))
                m = mm.find(mid)
                if m is None:
                    print("Member not found.")
                    continue

                lm.create(m, b)
                catalog.save_csv()
                mm.save_csv()
                lm.save_csv()

            except ValueError:
                print("Invalid input.")

        elif choice == "2":
            lm.show_active()
            try:
                lid = int(input("Loan ID to return: "))
                l = lm.find(lid)
                if l is None:
                    print("Loan not found.")
                elif l.returned:
                    print("Already returned.")
                else:
                    l.return_book()
                    catalog.save_csv()
                    mm.save_csv()
                    lm.save_csv()
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            lm.show_active()

        elif choice == "4":
            lm.show_overdue()

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def main():
    """The main entry point of the program. Launches the menu."""
    print("Welcome to Durak Library Management System")

    catalog = BookCatalog()
    mm = MemberManager()
    lm = LoanManager()

    print("\nLoading data...")
    load_data(catalog, mm)

    if len(catalog.books) == 0:
        print("No books found. Loading sample catalog...")
        setup_sample_books(catalog)
        catalog.save_csv()

    while True:
        print("\nMain Menu:")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Loan Management")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            book_management(catalog)
        elif choice == "2":
            member_management(mm)
        elif choice == "3":
            loan_management(catalog, mm, lm)
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Enter 0-3.")


if __name__ == "__main__":
    main()
