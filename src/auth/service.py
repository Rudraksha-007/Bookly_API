from src.db.models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from pydantic import EmailStr
from sqlmodel import select
from .utils import generate_phash


class UserService:
    async def get_user_by_email(self,email:str,session: AsyncSession):
        statement=select(User).where(User.email==email)
        # .options(selectinload(User.books))#type:ignore
        res=await session.exec(statement)
        return res.first()
    

    
    async def user_exists(self,email:str,session:AsyncSession):
        user=await self.get_user_by_email(email,session)
        if user is None:
            return False
        return True
    


    async def create_user(self,user_data:UserCreateModel,session:AsyncSession):
        user_data_dict=user_data.model_dump()
        new_user=User(
            **user_data_dict
        )
        
        new_user.password_hash=generate_phash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def update_user(self,user:User,update_data:dict,session:AsyncSession):
        for key,value in update_data.items():
            setattr(user,key,value)
            
        await session.commit()
        return user
