"""Chat data models."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common import BaseEntity


class MessageRole(str, Enum):
    """Message role enumeration."""
    
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSessionBase(BaseModel):
    """Base chat session model."""
    
    title: Optional[str] = Field(None, max_length=200)
    agent_id: UUID
    metadata: Dict = Field(default_factory=dict)


class ChatSessionCreate(ChatSessionBase):
    """Chat session creation model."""
    pass


class ChatSession(ChatSessionBase, BaseEntity):
    """Complete chat session model."""
    
    user_id: str
    is_active: bool = True
    message_count: int = 0
    
    class Config:
        """Pydantic config."""
        orm_mode = True


class ChatMessageBase(BaseModel):
    """Base chat message model."""
    
    content: str = Field(..., min_length=1)
    role: MessageRole
    metadata: Dict = Field(default_factory=dict)


class ChatMessageCreate(ChatMessageBase):
    """Chat message creation model."""
    
    session_id: UUID


class ChatMessage(ChatMessageBase, BaseEntity):
    """Complete chat message model."""
    
    session_id: UUID
    user_id: str
    response_time_ms: Optional[int] = None
    token_count: Optional[int] = None
    
    class Config:
        """Pydantic config."""
        orm_mode = True


class ChatResponse(BaseModel):
    """Chat response model."""
    
    message: ChatMessage
    agent_response: Optional[ChatMessage] = None
    session: ChatSession