from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.job import Job
from app.services.background_tasks import process_download_job

router = APIRouter()

class DownloadRequest(BaseModel):
    content_item_id: UUID

@router.post("")
async def download_content(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session)
):
    # Create Job
    job = Job(type="download", status="pending")
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    # Run in background
    background_tasks.add_task(process_download_job, str(job.id), str(request.content_item_id))
    
    return {"job_id": job.id, "status": "queued"}
