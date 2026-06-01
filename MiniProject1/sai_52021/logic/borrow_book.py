from logic.database import load_books, save_books
def borrow_book():
    books =load_books()
    book_id=input("enter id of the book to borrow: ")
    for book in books:
        if book["id"]==book_id:
            if book["copies"] >0:
                book["copies"]-=1
                save_books(books)
                print("book borrowed successfully")
            else:
                print("book not available")
            return
    print("book not found")
