from fastapi import FastAPI, Depends
from book import Book
from models import Books
from config import Session
from typing import List

app=FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.post('/add_new', response_model=Book)
def add_book(book: Book, db: Session = Depends(get_db)):
   bk=Books(id=book.id, title=book.title, author=book.author,
publisher=book.publisher)
   db.add(bk)
   db.commit()
   db.refresh(bk)
   return Books(**book.dict())

@app.get('/list', response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
   recs = db.query(Books).all()
   return recs

@app.get('/book/{id}', response_model=Book)
def get_book(id:int, db: Session = Depends(get_db)):
   return db.query(Books).filter(Books.id == id).first()

@app.put('/update/{id}', response_model=Book)
def update_book(id:int, book:Book, db: Session = Depends(get_db)):
   bk = db.query(Books).filter(Books.id == id).first()
   bk.id=book.id
   bk.title=book.title
   bk.author=book.author
   bk.publisher=book.publisher
   db.commit()
   return db.query(Books).filter(Books.id == id).first()

@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_db)):
   try:
      db.query(Books).filter(Books.id == id).delete()
      db.commit()
   except Exception as e:
      raise Exception(e)
   return {"delete status": "success"}

