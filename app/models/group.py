import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class GroupBase(SQLModel):
    name: str = Field(index=True, unique=True)  # Ex: "Culinária", "Finanças"
    description: Optional[str] = Field(default=None)
    status: str = Field(default="active", index=True)  # active, inactive

class Group(GroupBase, table=True):
    __tablename__ = "groups"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

