from logic.database import load_books, save_books
def return_book():
    books=load_books()
    book_id=input("enter id of the book to return: ")
    for book in books:
        if book["id"]==book_id:
            book["copies"]+=1
            save_books(books)
            print("book returned successfully")
            return
    print("book not found")     
