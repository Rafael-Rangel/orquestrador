from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.services.selector import SelectorService

router = APIRouter()

class SelectRequest(BaseModel):
    destination_id: UUID
    idempotency_key: UUID

@router.post("")
async def select_content(
    request: SelectRequest,
    session: AsyncSession = Depends(get_db_session)
):
    service = SelectorService(session)
    content = await service.select_content(request.destination_id, request.idempotency_key)
    
    if not content:
        return {"message": "No content available"}
        
    return content
