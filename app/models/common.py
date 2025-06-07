"""Common data models."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base entity with common fields."""
    
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic config."""
        orm_mode = True


class ResponseModel(BaseModel):
    """Standard response model."""
    
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[dict] = None