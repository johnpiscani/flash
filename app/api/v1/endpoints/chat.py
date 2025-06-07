"""Chat-related endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.chat import ChatMessage, ChatMessageCreate, ChatSession, ChatSessionCreate
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat/session", response_model=ChatSession, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    """Create a new chat session."""
    try:
        session = await chat_service.create_session(session_data, current_user["user_id"])
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create chat session: {str(e)}"
        )


@router.post("/chat/message", response_model=ChatMessage, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    """Send a message to the agent."""
    try:
        message = await chat_service.send_message(message_data, current_user["user_id"])
        return message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send message: {str(e)}"
        )


@router.get("/chat/history/{session_id}", response_model=List[ChatMessage])
async def get_chat_history(
    session_id: UUID,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    """Get chat history for a session."""
    try:
        messages = await chat_service.get_chat_history(
            session_id, 
            current_user["user_id"],
            skip=skip,
            limit=limit
        )
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get chat history: {str(e)}"
        )


@router.get("/chat/sessions", response_model=List[ChatSession])
async def list_chat_sessions(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    """List all chat sessions for the current user."""
    sessions = await chat_service.list_sessions(
        current_user["user_id"],
        skip=skip,
        limit=limit
    )
    return sessions


@router.delete("/chat/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    session_id: UUID,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(ChatService)
):
    """Delete a chat session."""
    success = await chat_service.delete_session(session_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )