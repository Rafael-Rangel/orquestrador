"""
Endpoints específicos para integração com n8n
Processa todos os grupos (nichos) automaticamente
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.job import Job
from app.models.group import Group
from app.models.source import Source
from app.services.background_tasks import process_n8n_fetch_job

router = APIRouter()

@router.post("/process-all-groups")
async def process_all_groups(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint principal para n8n
    Processa todos os grupos (nichos) ativos
    Verifica novas fontes e baixa vídeos organizados por grupo/fonte
    """
    # Create Job
    job = Job(type="n8n_fetch_all", status="pending")
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    # Run in background
    background_tasks.add_task(process_n8n_fetch_job, str(job.id))
    
    return {
        "job_id": job.id,
        "status": "queued",
        "message": "Processamento de todos os grupos iniciado"
    }

@router.get("/groups-summary")
async def get_groups_summary(
    session: AsyncSession = Depends(get_db_session)
):
    """
    Retorna resumo de todos os grupos para o n8n
    Útil para monitoramento e debugging
    """
    groups = await session.exec(
        select(Group).where(Group.status == "active")
    )
    
    result = []
    for group in groups.all():
        # Contar sources ativas
        sources = await session.exec(
            select(Source).where(
                Source.group_id == group.id,
                Source.status == "active"
            )
        )
        sources_list = list(sources.all())
        
        # Contar destinations
        from app.models.destination import Destination
        destinations = await session.exec(
            select(Destination).where(
                Destination.group_id == group.id,
                Destination.status == "active"
            )
        )
        destinations_list = list(destinations.all())
        
        result.append({
            "group_id": str(group.id),
            "group_name": group.name,
            "description": group.description,
            "sources_count": len(sources_list),
            "sources": [
                {
                    "id": str(s.id),
                    "platform": s.platform,
                    "external_id": s.external_id
                }
                for s in sources_list
            ],
            "destinations_count": len(destinations_list),
            "destinations": [
                {
                    "id": str(d.id),
                    "platform": d.platform,
                    "account_id": d.account_id
                }
                for d in destinations_list
            ]
        })
    
    return {
        "total_groups": len(result),
        "groups": result
    }

