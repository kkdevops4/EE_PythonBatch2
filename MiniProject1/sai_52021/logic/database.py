import json

DB_FILE = "books.json"

def load_books():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_books(books):
    with open(DB_FILE, "w") as f:
        json.dump(books, f, indent=4)
