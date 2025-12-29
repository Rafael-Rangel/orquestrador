from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session

async def get_db_session(session: AsyncSession = Depends(get_session)):
    return session
