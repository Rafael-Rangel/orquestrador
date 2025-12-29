"""
Endpoints para gerenciar Destinations (Canais de Destino) vinculados a Grupos
Estes são apenas etiquetas, não há lógica de publicação
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.destination import Destination
from app.models.group import Group

router = APIRouter()

class DestinationCreate(BaseModel):
    platform: str  # youtube, instagram, tiktok, etc
    account_id: str  # ID/username do canal de destino
    group_id: UUID  # ID do grupo (nicho) - funciona como etiqueta
    daily_limit: int = 1
    status: str = "active"

class DestinationUpdate(BaseModel):
    platform: Optional[str] = None
    account_id: Optional[str] = None
    group_id: Optional[UUID] = None
    daily_limit: Optional[int] = None
    status: Optional[str] = None

class DestinationResponse(BaseModel):
    id: UUID
    platform: str
    account_id: str
    group_id: UUID
    group_name: Optional[str] = None
    daily_limit: int
    status: str
    created_at: str

@router.post("", response_model=DestinationResponse)
async def create_destination(
    destination_data: DestinationCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """Cria um novo canal de destino (etiqueta)"""
    # Verificar se grupo existe
    group = await session.get(Group, destination_data.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    destination = Destination(**destination_data.dict())
    session.add(destination)
    await session.commit()
    await session.refresh(destination)
    
    return DestinationResponse(
        id=destination.id,
        platform=destination.platform,
        account_id=destination.account_id,
        group_id=destination.group_id,
        group_name=group.name,
        daily_limit=destination.daily_limit,
        status=destination.status,
        created_at=destination.created_at.isoformat()
    )

@router.get("", response_model=List[DestinationResponse])
async def list_destinations(
    group_id: Optional[UUID] = None,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session)
):
    """Lista todos os canais de destino, opcionalmente filtrados por grupo"""
    query = select(Destination)
    
    if group_id:
        query = query.where(Destination.group_id == group_id)
    if status:
        query = query.where(Destination.status == status)
    
    destinations = await session.exec(query)
    result = []
    
    for destination in destinations.all():
        group = await session.get(Group, destination.group_id)
        result.append(DestinationResponse(
            id=destination.id,
            platform=destination.platform,
            account_id=destination.account_id,
            group_id=destination.group_id,
            group_name=group.name if group else None,
            daily_limit=destination.daily_limit,
            status=destination.status,
            created_at=destination.created_at.isoformat()
        ))
    
    return result

@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Obtém um canal de destino específico"""
    destination = await session.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Canal de destino não encontrado")
    
    group = await session.get(Group, destination.group_id)
    
    return DestinationResponse(
        id=destination.id,
        platform=destination.platform,
        account_id=destination.account_id,
        group_id=destination.group_id,
        group_name=group.name if group else None,
        daily_limit=destination.daily_limit,
        status=destination.status,
        created_at=destination.created_at.isoformat()
    )

@router.put("/{destination_id}", response_model=DestinationResponse)
async def update_destination(
    destination_id: UUID,
    destination_data: DestinationUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    """Atualiza um canal de destino"""
    destination = await session.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Canal de destino não encontrado")
    
    # Se group_id foi alterado, verificar se existe
    if destination_data.group_id:
        group = await session.get(Group, destination_data.group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # Atualizar campos
    update_data = destination_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(destination, field, value)
    
    session.add(destination)
    await session.commit()
    await session.refresh(destination)
    
    group = await session.get(Group, destination.group_id)
    
    return DestinationResponse(
        id=destination.id,
        platform=destination.platform,
        account_id=destination.account_id,
        group_id=destination.group_id,
        group_name=group.name if group else None,
        daily_limit=destination.daily_limit,
        status=destination.status,
        created_at=destination.created_at.isoformat()
    )

@router.delete("/{destination_id}")
async def delete_destination(
    destination_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Deleta um canal de destino"""
    destination = await session.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Canal de destino não encontrado")
    
    await session.delete(destination)
    await session.commit()
    
    return {"status": "deleted", "message": "Canal de destino deletado com sucesso"}

