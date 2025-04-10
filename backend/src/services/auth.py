from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import User
from src.schemas.users import UserCreate
from src.auth.auth import hash_password
from sqlmodel import select
from fastapi import HTTPException

class UserService:
    async def get_user_by_username(self, username: str, db: AsyncSession) -> User | None:
        """Obtiene un usuario por su nombre de usuario."""
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    async def user_exists(self, username: str, db: AsyncSession) -> bool:
        """Verifica si un usuario ya existe en la base de datos."""
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first() is not None

    async def create_user(self, user_data: UserCreate, db: AsyncSession) -> User:
        """Crea un nuevo usuario en la base de datos."""
        password_hash = hash_password(user_data.password)
        new_user = User(username=user_data.username, password_hash=password_hash)
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user