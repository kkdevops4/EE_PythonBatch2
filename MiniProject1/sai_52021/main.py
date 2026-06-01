from logic.addbook import add_book
from logic.display import display_books
from logic.borrow_book import borrow_book
from logic.returns import return_book
from logic.genre import genre
from logic.search import search_author
from logic.database import load_books, save_books


def main():
    load_books()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search by Author")
        print("6. Search by Genre")
        print("7. Exit")

        choice = input("enter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            display_books()

        elif choice == "3":
            borrow_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            search_author()

        elif choice == "6":
            genre()

        elif choice == "7":
            save_books()
            print("exiting the program...")
            break

        else:
            print("invalid choice, please try again.")
            
if __name__ == "__main__":
    main()
