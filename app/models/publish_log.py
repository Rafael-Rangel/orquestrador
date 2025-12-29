import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class PublishLogBase(SQLModel):
    destination_id: uuid.UUID = Field(foreign_key="destinations.id")
    content_item_id: uuid.UUID = Field(foreign_key="content_items.id")
    published_at: datetime = Field(default_factory=datetime.utcnow)
    platform_post_id: Optional[str] = Field(default=None)
    result: str = Field(index=True) # success, error

class PublishLog(PublishLogBase, table=True):
    __tablename__ = "publish_logs"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
