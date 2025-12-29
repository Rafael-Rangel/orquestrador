import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class DestinationBase(SQLModel):
    platform: str = Field(index=True)  # youtube, instagram, tiktok, etc
    account_id: str = Field(index=True)  # ID/username do canal de destino
    group_id: uuid.UUID = Field(foreign_key="groups.id", index=True)  # Nicho ao qual pertence (etiqueta)
    daily_limit: int = Field(default=1)
    status: str = Field(default="active", index=True)
    # Mantido para compatibilidade, mas será substituído por group_id
    niche: Optional[str] = Field(default=None, index=True)

class Destination(DestinationBase, table=True):
    __tablename__ = "destinations"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
