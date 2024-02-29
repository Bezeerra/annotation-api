from sqlalchemy import or_, select, and_

from app.func_db.utils import BaseFuncDB, get_hash_by_key
from models.user import User


class UserDB(BaseFuncDB):
    def __init__(self, settings):
        super().__init__(settings)

    async def create(self, user: User) -> User:
        async with self.settings.session_db() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: str) -> User:
        query = select(User).where(User.id == user_id)
        async with self.settings.session_db() as session:
            return (await session.execute(query)).scalars().first()

    async def get_user_by_email_or_name(self, email: str, name: str) -> User:
        query = select(User).where(or_(User.email == email, User.name == name))
        async with self.settings.session_db() as session:
            return (await session.execute(query)).scalars().first()

    async def get_user_email_password(self, email: str, password: str) -> User:
        password = await get_hash_by_key(password)
        query = select(User).where(and_(User.email == email, User.password == password))
        async with self.settings.session_db() as session:
            return (await session.execute(query)).scalars().first()

    async def get_all_users(self) -> list[User]:
        async with self.settings.session_db() as session:
            return (await session.execute(select(User))).scalars().all()

    async def update(
        self, user: User
    ) -> User:  # WRONG IMPLEMENTATION - need filter empty keys
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def delete(
        self, user: User
    ) -> User:  # WRONG IMPLEMENTATION - need filter empty keys
        await self.db_session.delete(user)
        await self.db_session.commit()
        return user
