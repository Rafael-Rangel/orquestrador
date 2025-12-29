from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.dependencies import get_db_session
from app.models.job import Job
from app.services.background_tasks import process_fetch_job

router = APIRouter()

@router.post("/run")
async def run_fetch(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session)
):
    # Create Job
    job = Job(type="fetch", status="pending")
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    # Run in background (simple async task)
    background_tasks.add_task(process_fetch_job, str(job.id))
    
    return {"job_id": job.id, "status": "queued"}
