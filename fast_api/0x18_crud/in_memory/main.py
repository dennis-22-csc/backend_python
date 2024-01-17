from fastapi import FastAPI
from book import Book

app = FastAPI()

books = []

@app.post("/book")
def add_book(book: Book):
   books.append(book.dict())
   return books

@app.get("/list")
def get_books():
   return books

@app.get("/book/{id}")
def get_book(id: int):
   id = id - 1
   return books[id]

@app.put("/book/{id}")
def add_book(id: int, book: Book):
   books[id-1] = book
   return books

@app.delete("/book/{id}")
def delete_book(id: int):
   books.pop(id-1)
   return books
