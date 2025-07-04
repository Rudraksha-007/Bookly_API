from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.db.models import Book
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession,limit: int = 10, offset: int = 0):
        statement = select(Book).order_by(desc(Book.created_at)).offset(offset).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_books(self, book_id: str, session: AsyncSession):
        statemet = select(Book).where(Book.uid == book_id)
        result = await session.exec(statemet)
        book = result.first()
        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()
        published_date = book_data_dict["published_date"]
        
        if isinstance(published_date, str):
            new_book = Book(**book_data_dict)
            new_book.published_date = datetime.strptime(published_date, "%Y-%m-%d")
        else:
            new_book = Book(**book_data_dict)

        new_book.user_uid = user_uid  # type:ignore
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_id: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_books(book_id, session)
        if book_to_update is None:
            return None
        update_data_dict = update_data.model_dump()
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        await session.commit()
        return book_to_update

    async def delete_book(self, book_id: str, session: AsyncSession):
        getrid = await self.get_books(book_id, session)
        if getrid is not None:
            await session.delete(getrid)
            await session.commit()
            return {}
        else:
            return None

    async def get_user_books(self, user_id: str, session: AsyncSession):
        statement = select(Book).where(user_id == Book.user_uid)
        return await session.exec(statement)
