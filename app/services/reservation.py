from datetime import datetime, timedelta
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.content_item import ContentItem

class ReservationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def reserve_content(self, content_item: ContentItem, minutes: int = 30):
        content_item.reserved_until = datetime.utcnow() + timedelta(minutes=minutes)
        self.session.add(content_item)
        await self.session.commit()
        await self.session.refresh(content_item)
    
    async def release_reservation(self, content_item: ContentItem):
        content_item.reserved_until = None
        self.session.add(content_item)
        await self.session.commit()
