from fastapi import APIRouter, Depends
from src.db.models import User, Reviews
from src.db.main import get_session
from src.auth.dependencies import get_curr_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from src.reviews.service import ReviewService

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_id}")
async def add_review_to_book(
    book_id: str,
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    curr_user: User=Depends(get_curr_user)
):
    curr=curr_user.model_dump()
    email = curr["email"]  # type: ignore
    newRev = await review_service.add_review_to_book(
        user_email=email, book_id=book_id, review_data=review_data, session=session
    )
    return newRev 
