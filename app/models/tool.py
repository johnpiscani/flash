"""Tool data models."""

from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common import BaseEntity


class ToolBase(BaseModel):
    """Base tool model."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tool_type: str = Field(..., min_length=1, max_length=50)
    category: str = Field(default="Utility")
    configuration: Dict = Field(default_factory=dict)
    is_enabled: bool = Field(default=True)
    metadata: Dict = Field(default_factory=dict)


class ToolCreate(ToolBase):
    """Tool creation model."""
    pass


class ToolUpdate(BaseModel):
    """Tool update model."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tool_type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = None
    configuration: Optional[Dict] = None
    is_enabled: Optional[bool] = None
    metadata: Optional[Dict] = None


class Tool(ToolBase, BaseEntity):
    """Complete tool model."""
    
    user_id: str
    is_active: bool = True
    
    class Config:
        """Pydantic config."""
        orm_mode = True