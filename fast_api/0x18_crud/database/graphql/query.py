import strawberry
from book import Book
from typing import List
from fastapi import HTTPException

books = [
    Book(id=1, title="Computer Fundamentals", author="Sinha", price=300),
    Book(id=2, title="Introduction to Python", author="Smith", price=250),
    Book(id=3, title="Web Development Basics", author="Johnson", price=400),
]
@strawberry.type
class Query:
    @strawberry.field
    def book(self, book_id: int) -> Book:
        for book in books:
            if book.id == book_id:
                return book
        raise HTTPException(status_code=404, detail="Book not found")

    @strawberry.field
    def books(self) -> List[Book]:
        return books

