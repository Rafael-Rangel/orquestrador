import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

class SourceBase(SQLModel):
    platform: str = Field(index=True)  # youtube, instagram, tiktok, etc
    external_id: str = Field(index=True)  # ID/username do canal
    group_id: uuid.UUID = Field(foreign_key="groups.id", index=True)  # Nicho ao qual pertence
    status: str = Field(default="active", index=True)
    license_status: Optional[str] = Field(default=None)
    # Mantido para compatibilidade, mas será substituído por group_id
    niche: Optional[str] = Field(default=None, index=True)

class Source(SourceBase, table=True):
    __tablename__ = "sources"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
