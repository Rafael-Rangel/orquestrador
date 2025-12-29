import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models.source import Source

class ContentItemBase(SQLModel):
    platform: str = Field(index=True)
    external_video_id: str = Field(index=True, unique=True)
    source_id: uuid.UUID = Field(foreign_key="sources.id")
    published_at: datetime = Field(index=True) # Original publish date
    content_hash: Optional[str] = Field(default=None, index=True)
    storage_path: Optional[str] = Field(default=None)
    status: str = Field(default="discovered", index=True) # discovered, downloaded, published, error
    reserved_until: Optional[datetime] = Field(default=None)
    reserved_by_destination_id: Optional[uuid.UUID] = Field(default=None, foreign_key="destinations.id", index=True)

class ContentItem(ContentItemBase, table=True):
    __tablename__ = "content_items"
    __table_args__ = (UniqueConstraint("platform", "external_video_id", name="unique_content_item"),)
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    # source: Source = Relationship()
