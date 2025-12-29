"""
Endpoints para gerenciar Grupos (Nichos)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.group import Group
from app.models.source import Source
from app.models.destination import Destination

router = APIRouter()

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class GroupResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str
    sources_count: int = 0
    destinations_count: int = 0

@router.post("", response_model=GroupResponse)
async def create_group(
    group_data: GroupCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """Cria um novo grupo (nicho)"""
    # Verificar se já existe grupo com mesmo nome
    existing = await session.exec(
        select(Group).where(Group.name == group_data.name)
    )
    if existing.first():
        raise HTTPException(status_code=400, detail="Grupo com este nome já existe")
    
    group = Group(**group_data.dict())
    session.add(group)
    await session.commit()
    await session.refresh(group)
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        status=group.status,
        created_at=group.created_at.isoformat(),
        updated_at=group.updated_at.isoformat(),
        sources_count=0,
        destinations_count=0
    )

@router.get("", response_model=List[GroupResponse])
async def list_groups(
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session)
):
    """Lista todos os grupos"""
    query = select(Group)
    if status:
        query = query.where(Group.status == status)
    
    groups = await session.exec(query)
    result = []
    
    for group in groups.all():
        # Contar sources e destinations
        sources_count = await session.exec(
            select(Source).where(Source.group_id == group.id)
        )
        destinations_count = await session.exec(
            select(Destination).where(Destination.group_id == group.id)
        )
        
        result.append(GroupResponse(
            id=group.id,
            name=group.name,
            description=group.description,
            status=group.status,
            created_at=group.created_at.isoformat(),
            updated_at=group.updated_at.isoformat(),
            sources_count=len(list(sources_count.all())),
            destinations_count=len(list(destinations_count.all()))
        ))
    
    return result

@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Obtém um grupo específico"""
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    sources_count = await session.exec(
        select(Source).where(Source.group_id == group.id)
    )
    destinations_count = await session.exec(
        select(Destination).where(Destination.group_id == group.id)
    )
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        status=group.status,
        created_at=group.created_at.isoformat(),
        updated_at=group.updated_at.isoformat(),
        sources_count=len(list(sources_count.all())),
        destinations_count=len(list(destinations_count.all()))
    )

@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: UUID,
    group_data: GroupUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    """Atualiza um grupo"""
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # Atualizar campos fornecidos
    update_data = group_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    
    from datetime import datetime
    group.updated_at = datetime.utcnow()
    
    session.add(group)
    await session.commit()
    await session.refresh(group)
    
    sources_count = await session.exec(
        select(Source).where(Source.group_id == group.id)
    )
    destinations_count = await session.exec(
        select(Destination).where(Destination.group_id == group.id)
    )
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        status=group.status,
        created_at=group.created_at.isoformat(),
        updated_at=group.updated_at.isoformat(),
        sources_count=len(list(sources_count.all())),
        destinations_count=len(list(destinations_count.all()))
    )

@router.delete("/{group_id}")
async def delete_group(
    group_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Deleta um grupo (apenas se não tiver sources ou destinations)"""
    group = await session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # Verificar se tem sources ou destinations
    sources = await session.exec(
        select(Source).where(Source.group_id == group.id)
    )
    destinations = await session.exec(
        select(Destination).where(Destination.group_id == group.id)
    )
    
    if list(sources.all()) or list(destinations.all()):
        raise HTTPException(
            status_code=400,
            detail="Não é possível deletar grupo que possui sources ou destinations. Remova-os primeiro."
        )
    
    await session.delete(group)
    await session.commit()
    
    return {"status": "deleted", "message": "Grupo deletado com sucesso"}

