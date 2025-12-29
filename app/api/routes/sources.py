"""
Endpoints para gerenciar Sources (Fontes) vinculadas a Grupos
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.source import Source
from app.models.group import Group

router = APIRouter()

class SourceCreate(BaseModel):
    platform: str  # youtube, instagram, tiktok, etc
    external_id: str  # ID/username do canal
    group_id: UUID  # ID do grupo (nicho)
    status: str = "active"
    license_status: Optional[str] = None

class SourceUpdate(BaseModel):
    platform: Optional[str] = None
    external_id: Optional[str] = None
    group_id: Optional[UUID] = None
    status: Optional[str] = None
    license_status: Optional[str] = None

class SourceResponse(BaseModel):
    id: UUID
    platform: str
    external_id: str
    group_id: UUID
    group_name: Optional[str] = None
    status: str
    license_status: Optional[str]
    created_at: str

@router.post("", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """Cria uma nova fonte (canal de origem)"""
    # Verificar se grupo existe
    group = await session.get(Group, source_data.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    source = Source(**source_data.dict())
    session.add(source)
    await session.commit()
    await session.refresh(source)
    
    return SourceResponse(
        id=source.id,
        platform=source.platform,
        external_id=source.external_id,
        group_id=source.group_id,
        group_name=group.name,
        status=source.status,
        license_status=source.license_status,
        created_at=source.created_at.isoformat()
    )

@router.get("", response_model=List[SourceResponse])
async def list_sources(
    group_id: Optional[UUID] = None,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session)
):
    """Lista todas as fontes, opcionalmente filtradas por grupo"""
    query = select(Source)
    
    if group_id:
        query = query.where(Source.group_id == group_id)
    if status:
        query = query.where(Source.status == status)
    
    sources = await session.exec(query)
    result = []
    
    for source in sources.all():
        group = await session.get(Group, source.group_id)
        result.append(SourceResponse(
            id=source.id,
            platform=source.platform,
            external_id=source.external_id,
            group_id=source.group_id,
            group_name=group.name if group else None,
            status=source.status,
            license_status=source.license_status,
            created_at=source.created_at.isoformat()
        ))
    
    return result

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Obtém uma fonte específica"""
    source = await session.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Fonte não encontrada")
    
    group = await session.get(Group, source.group_id)
    
    return SourceResponse(
        id=source.id,
        platform=source.platform,
        external_id=source.external_id,
        group_id=source.group_id,
        group_name=group.name if group else None,
        status=source.status,
        license_status=source.license_status,
        created_at=source.created_at.isoformat()
    )

@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: UUID,
    source_data: SourceUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    """Atualiza uma fonte"""
    source = await session.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Fonte não encontrada")
    
    # Se group_id foi alterado, verificar se existe
    if source_data.group_id:
        group = await session.get(Group, source_data.group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # Atualizar campos
    update_data = source_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(source, field, value)
    
    session.add(source)
    await session.commit()
    await session.refresh(source)
    
    group = await session.get(Group, source.group_id)
    
    return SourceResponse(
        id=source.id,
        platform=source.platform,
        external_id=source.external_id,
        group_id=source.group_id,
        group_name=group.name if group else None,
        status=source.status,
        license_status=source.license_status,
        created_at=source.created_at.isoformat()
    )

@router.delete("/{source_id}")
async def delete_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    """Deleta uma fonte"""
    source = await session.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Fonte não encontrada")
    
    await session.delete(source)
    await session.commit()
    
    return {"status": "deleted", "message": "Fonte deletada com sucesso"}

