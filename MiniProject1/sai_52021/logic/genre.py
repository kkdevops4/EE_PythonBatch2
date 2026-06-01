from logic.database import load_books, save_books
def genre():
    book=load_books()
    genre=input("enter genre to search: ")
    for book in book:
        if book["genre"].lower()==genre.lower():
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Copies: {book['copies']}")
            return True
    print("book not found")
    return False        
