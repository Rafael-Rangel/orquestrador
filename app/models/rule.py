import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

class RuleBase(SQLModel):
    destination_id: Optional[uuid.UUID] = Field(default=None, foreign_key="destinations.id")
    niche: Optional[str] = Field(default=None, index=True)
    weight: int = Field(default=1)
    cooldown_hours: int = Field(default=24)
    priority: int = Field(default=0)

class Rule(RuleBase, table=True):
    __tablename__ = "rules"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    )
