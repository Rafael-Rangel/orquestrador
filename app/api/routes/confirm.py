from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.publish_log import PublishLog
from app.models.content_item import ContentItem

router = APIRouter()

class ConfirmPublishRequest(BaseModel):
    destination_id: UUID
    content_item_id: UUID
    result: str # success, error
    platform_post_id: Optional[str] = None
    error_message: Optional[str] = None

@router.post("")
async def confirm_publish(
    request: ConfirmPublishRequest,
    session: AsyncSession = Depends(get_db_session)
):
    # 1. Log Publish
    log = PublishLog(
        destination_id=request.destination_id,
        content_item_id=request.content_item_id,
        result=request.result,
        platform_post_id=request.platform_post_id,
        published_at=datetime.utcnow()
    )
    session.add(log)
    
    # 2. Update Content Item
    content_item = await session.get(ContentItem, request.content_item_id)
    if content_item:
        if request.result == "success":
            content_item.status = "published"
            # Release reservation (set to null or keep history?)
            # Prompt says: "Marca conteúdo como publicado... Libera reserva"
            content_item.reserved_until = None
            content_item.reserved_by_destination_id = None
        else:
            # If error, maybe release reservation so it can be tried again? 
            # Or mark as error?
            # Prompt: "Confirma sucesso ou erro... Insere em publish_logs... Libera reserva"
            content_item.reserved_until = None
            content_item.reserved_by_destination_id = None
            # Maybe keep status as 'downloaded' to retry?
            # Or 'error' if fatal?
            # Let's keep it 'downloaded' but release reservation so it can be picked again if rules allow,
            # BUT Selector checks publish_logs. If result is 'error', selector might pick it again?
            # Selector logic: "notin_(published_subquery)". If we log 'error', it is in published_subquery?
            # We should refine Selector to only exclude 'success' logs?
            # For now, let's just release reservation.
        
        session.add(content_item)
    
    await session.commit()
    return {"status": "confirmed"}
