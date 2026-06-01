from logic.database import load_books
def search_author():
    books=load_books()
    author=input("enter author name to search: ")
    found=False
    for book in books:
        if book["author"].lower()==author.lower():
            print(f"ID: {book['id']}, Title: {book['title']}, Genre: {book['genre']}, Copies: {book['copies']}")
            found=True
    if not found:
        print("book not found")
