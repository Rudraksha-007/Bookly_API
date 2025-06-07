from fastapi import APIRouter
from fastapi import FastAPI, Header, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.books.data import data
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import get_curr_user, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_service =Depends(RoleChecker(["admin", "user"]))


@book_router.get("/", response_model=List[Book],dependencies=[role_service])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_Details=Depends(access_token_bearer),
    _:bool = Depends(role_service)
):
    print(user_Details)
    book = await book_service.get_all_books(session)
    return book


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book,dependencies=[role_service])
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_Details=Depends(access_token_bearer),
):
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_id}", response_model=Book,dependencies=[role_service])
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_Details=Depends(access_token_bearer),
):
    book = await book_service.get_books(str(book_id), session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_id}",dependencies=[role_service])
async def update_book(
    book_id: str,
    update_info: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_Details=Depends(access_token_bearer),
):

    updatedBook = await book_service.update_book(str(book_id), update_info, session)
    if updatedBook:
        return updatedBook
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book was not located."
        )


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT,dependencies=[role_service])
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_Details=Depends(access_token_bearer),
):
    getrid = await book_service.delete_book(str(book_id), session)
    if getrid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return None
