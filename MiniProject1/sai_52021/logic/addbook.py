from logic.database import load_books, save_books
def add_book():
    books=load_books()
    book_id=input("enter id of the book: ")
    title=input("enter title of the book: ")    
    author=input("enter author of the book: ")
    genre=input("enter genre of the book: ")
    copies=int(input("enter number of copies of the book: "))
    new_book={
        "id":book_id,
        "title":title,  
        "author":author,
        "genre":genre,
        "copies":copies 
    }
    books.append(new_book)
    save_books(books)
    print("book added successfully")