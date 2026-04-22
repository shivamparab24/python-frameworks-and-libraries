from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from FastAPI.Ssali_Jonathan.CRUD.auth.user_models import User
from FastAPI.Ssali_Jonathan.CRUD.auth.user_schema import UserCreateModel
from FastAPI.Ssali_Jonathan.CRUD.utils.utils import generate_paswd_hash

class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statenment = select(User).where(User.email == email)

        result = await session.execute(statenment)

        user = result.scalar_one_or_none()

        return user
    

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        # if user is None:
        #     return False
        # else:
        #     return True
        
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        password = user_data_dict.pop("password")

        new_user = User(
            **user_data_dict
        )

        new_user.password_hash = generate_paswd_hash(password)
        new_user.role = 'user'

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
    
    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        
        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user