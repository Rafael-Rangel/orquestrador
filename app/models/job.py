import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class JobBase(SQLModel):
    type: str = Field(index=True) # fetch, download
    status: str = Field(index=True, default="pending") # pending, running, completed, failed
    retries: int = Field(default=0)
    error_message: Optional[str] = Field(default=None)

class Job(JobBase, table=True):
    __tablename__ = "jobs"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
