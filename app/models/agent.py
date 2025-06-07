"""Agent data models."""

from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common import BaseEntity


class AgentBase(BaseModel):
    """Base agent model."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    system_prompt: str = Field(..., min_length=1)
    model_name: str = Field(default="gemini-pro")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, gt=0)
    tools: List[str] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


class AgentCreate(AgentBase):
    """Agent creation model."""
    pass


class AgentUpdate(BaseModel):
    """Agent update model."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    system_prompt: Optional[str] = Field(None, min_length=1)
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    tools: Optional[List[str]] = None
    metadata: Optional[Dict] = None


class Agent(AgentBase, BaseEntity):
    """Complete agent model."""
    
    user_id: str
    is_active: bool = True
    
    class Config:
        """Pydantic config."""
        orm_mode = True