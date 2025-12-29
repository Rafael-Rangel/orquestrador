from datetime import datetime, timedelta
import logging
from typing import Optional
from uuid import UUID
from sqlmodel import select, col, and_, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.content_item import ContentItem
from app.models.destination import Destination
from app.models.publish_log import PublishLog
from app.models.rule import Rule
from app.models.idempotency_key import IdempotencyKey

logger = logging.getLogger(__name__)

class SelectorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def select_content(self, destination_id: UUID, idempotency_key: UUID) -> Optional[ContentItem]:
        # 1. Get Destination
        destination = await self.session.get(Destination, destination_id)
        if not destination:
            raise ValueError("Destination not found")

        # 1.1 Idempotency: if key exists, return same item
        existing_key = await self.session.exec(
            select(IdempotencyKey).where(
                IdempotencyKey.key == idempotency_key,
                IdempotencyKey.destination_id == destination_id
            )
        )
        existing_key = existing_key.first()
        if existing_key:
            item = await self.session.get(ContentItem, existing_key.content_item_id)
            if item:
                return item

        # 2. Get Rules for Destination
        # Rules can be specific to destination or by niche
        rules_stmt = select(Rule).where(
            or_(
                Rule.destination_id == destination_id,
                Rule.niche == destination.niche
            )
        ).order_by(col(Rule.priority).desc())
        
        rules_result = await self.session.exec(rules_stmt)
        rules = rules_result.all()

        # 3. Find Candidate Content
        # Must be:
        # - status = 'discovered' (or maybe 'downloaded' if we support pre-download)
        # - not reserved (reserved_until < now or null)
        # - not published to this destination (check publish_logs)
        
        # We need to exclude content already published to this destination
        published_subquery = select(PublishLog.content_item_id).where(
            PublishLog.destination_id == destination_id,
            PublishLog.result == "success"
        )
        
        # Basic query
        query = select(ContentItem).where(
            ContentItem.status == "discovered",
            or_(
                ContentItem.reserved_until == None,
                ContentItem.reserved_until < datetime.utcnow()
            ),
            col(ContentItem.id).notin_(published_subquery),
            or_(
                ContentItem.reserved_by_destination_id == None,
                ContentItem.reserved_by_destination_id == destination_id
            )
        )
        
        # Filter by niche via Source (needs join)
        # Assuming ContentItem -> Source relationship
        # For simplicity, we assume we filter by logic or join.
        # Let's add a join if we need to filter by source niche matching destination niche
        # query = query.join(Source).where(Source.niche == destination.niche)
        
        # Order by published_at (oldest first? or newest?)
        # Usually oldest first to clear backlog, or newest for trends.
        # Let's go with published_at desc (newest)
        query = query.order_by(col(ContentItem.published_at).desc())
        
        result = await self.session.exec(query)
        candidate = result.first()
        
        if candidate:
            # 4. Reserve Content
            candidate.reserved_until = datetime.utcnow() + timedelta(minutes=30) # 30 min reservation
            candidate.reserved_by_destination_id = destination_id
            self.session.add(candidate)
            await self.session.commit()
            await self.session.refresh(candidate)
            # Save Idempotency key
            idem = IdempotencyKey(
                key=idempotency_key,
                destination_id=destination_id,
                content_item_id=candidate.id
            )
            self.session.add(idem)
            await self.session.commit()
            return candidate
            
        return None
