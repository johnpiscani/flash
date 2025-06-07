"""Chat service for managing chat sessions and messages."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.chat import (
    ChatMessage, 
    ChatMessageCreate, 
    ChatSession, 
    ChatSessionCreate,
    MessageRole
)
from app.services.agent_service import AgentService
from app.services.llm_service import LLMService


class ChatService:
    """Service for managing chat sessions and messages."""
    
    def __init__(self):
        """Initialize chat service."""
        self.agent_service = AgentService()
        self.llm_service = LLMService()
        # In a real application, you would inject database services here
        self._sessions_storage = {}  # Temporary in-memory storage
        self._messages_storage = {}  # Temporary in-memory storage
    
    async def create_session(
        self, 
        session_data: ChatSessionCreate, 
        user_id: str
    ) -> ChatSession:
        """Create a new chat session."""
        # Verify agent exists and belongs to user
        agent = await self.agent_service.get_agent(session_data.agent_id, user_id)
        if not agent:
            raise ValueError("Agent not found or access denied")
        
        session = ChatSession(
            **session_data.dict(),
            user_id=user_id
        )
        
        # Store session
        self._sessions_storage[str(session.id)] = session
        
        return session
    
    async def send_message(
        self, 
        message_data: ChatMessageCreate, 
        user_id: str
    ) -> ChatMessage:
        """Send a message and get agent response."""
        # Verify session exists and belongs to user
        session = self._sessions_storage.get(str(message_data.session_id))
        if not session or session.user_id != user_id:
            raise ValueError("Session not found or access denied")
        
        # Get agent
        agent = await self.agent_service.get_agent(session.agent_id, user_id)
        if not agent:
            raise ValueError("Agent not found")
        
        # Create user message
        user_message = ChatMessage(
            **message_data.dict(),
            user_id=user_id
        )
        
        # Store user message
        self._messages_storage[str(user_message.id)] = user_message
        
        # Get chat history
        chat_history = await self.get_chat_history(
            message_data.session_id, 
            user_id, 
            limit=10
        )
        
        # Generate agent response
        try:
            llm_response = await self.llm_service.generate_response(
                agent=agent,
                message=message_data.content,
                chat_history=chat_history
            )
            
            # Create agent response message
            agent_message = ChatMessage(
                content=llm_response["content"],
                role=MessageRole.ASSISTANT,
                session_id=message_data.session_id,
                user_id=user_id,
                response_time_ms=llm_response.get("response_time_ms"),
                token_count=llm_response.get("token_count")
            )
            
            # Store agent message
            self._messages_storage[str(agent_message.id)] = agent_message
            
            # Update session message count
            session.message_count += 2
            session.updated_at = datetime.utcnow()
            
            return agent_message
            
        except Exception as e:
            raise Exception(f"Failed to generate agent response: {str(e)}")
    
    async def get_chat_history(
        self, 
        session_id: UUID, 
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get chat history for a session."""
        # Verify session access
        session = self._sessions_storage.get(str(session_id))
        if not session or session.user_id != user_id:
            raise ValueError("Session not found or access denied")
        
        # Get messages for session
        session_messages = [
            msg for msg in self._messages_storage.values()
            if msg.session_id == session_id
        ]
        
        # Sort by creation time
        session_messages.sort(key=lambda x: x.created_at)
        
        return session_messages[skip:skip + limit]
    
    async def list_sessions(
        self, 
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatSession]:
        """List all chat sessions for a user."""
        user_sessions = [
            session for session in self._sessions_storage.values()
            if session.user_id == user_id and session.is_active
        ]
        
        # Sort by updated time (most recent first)
        user_sessions.sort(key=lambda x: x.updated_at or x.created_at, reverse=True)
        
        return user_sessions[skip:skip + limit]
    
    async def delete_session(self, session_id: UUID, user_id: str) -> bool:
        """Delete a chat session."""
        session = self._sessions_storage.get(str(session_id))
        if not session or session.user_id != user_id:
            return False
        
        # Soft delete
        session.is_active = False
        session.updated_at = datetime.utcnow()
        
        return True