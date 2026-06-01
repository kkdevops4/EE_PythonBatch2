from logic.database import load_books, save_books
def display_books():
    books=load_books()
    if len(books)==0:
        print("no books available")
    if len(books)>0:
        for book in books:
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}, Copies: {book['copies']}")
