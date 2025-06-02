from fastapi import APIRouter
from fastapi import FastAPI,Header,status,HTTPException
from fastapi.responses import JSONResponse
from src.books.data import data
from src.books.schemas import Book,Bookupdate
from typing import List

book_router=APIRouter()
@book_router.get('/')
async def index():
    return {"message":"Hello World"}

@book_router.get("/",response_model=List[Book])
def get_all_books():
    return data

@book_router.post("/",status_code=status.HTTP_201_CREATED)
def create_book(book_data:Book):
    new_book=book_data.model_dump()
    data.append(new_book)
    return new_book

@book_router.get("/{book_id}")
def get_book(book_id:int):
    for book in data:
        if book["id"]==book_id:
            return book
    return JSONResponse(content={"Error":"Book cannot be located"},status_code=404)

@book_router.patch("/{book_id}")
def update_book(book_id:int , update_info:Bookupdate)->dict:
    for book in data:
        if book["id"]==book_id:
            book["publisher"]=update_info.publisher
            book["published_date"]=update_info.published_date
            book['page_count']=update_info.page_count
            book['language']=update_info.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book was not located.")

@book_router.delete("/{book_id}")
def delete_book(book_id:int):
    for book in data:
        if book["id"]==book_id:
            data.remove(book)
            return JSONResponse(content={"Status":f"the Book with book id = {book_id} was deleted."},status_code=status.HTTP_410_GONE)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)    