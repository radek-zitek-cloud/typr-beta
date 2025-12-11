from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get(db: AsyncSession, id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_multi(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create(db: AsyncSession, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        # Hash password here
        hashed_password=obj_in.password,  # Use proper hashing!
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj