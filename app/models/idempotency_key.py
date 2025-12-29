import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class IdempotencyKey(SQLModel, table=True):
    __tablename__ = "idempotency_keys"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    key: uuid.UUID = Field(index=True)
    destination_id: uuid.UUID = Field(foreign_key="destinations.id", index=True)
    content_item_id: uuid.UUID = Field(foreign_key="content_items.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

