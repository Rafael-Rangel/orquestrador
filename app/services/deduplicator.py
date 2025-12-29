from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.content_item import ContentItem

class DeduplicatorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_duplicate_hash(self, content_hash: str) -> bool:
        stmt = select(ContentItem).where(ContentItem.content_hash == content_hash)
        result = await self.session.exec(stmt)
        return result.first() is not None
