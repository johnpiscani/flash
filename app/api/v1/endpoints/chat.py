"""Chat-related endpoints."""

from typing import List

from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Mock data for development
mock_sessions = []
mock_messages = []
session_counter = 1
message_counter = 1


@router.post("/chat/message", response_model=dict, status_code=status.HTTP_201_CREATED)
async def send_message(message_data: dict):
    """Send a message to the agent."""
    global message_counter
    try:
        # Create mock response
        user_message = {
            "id": message_counter,
            "role": "user",
            "message": message_data.get("message", ""),
            "timestamp": "2024-01-01T00:00:00Z"
        }
        message_counter += 1
        
        # Create mock agent response
        agent_response = {
            "id": message_counter,
            "role": "assistant",
            "message": f"I received your message: '{message_data.get('message', '')}'. This is a mock response from the agent.",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        message_counter += 1
        
        mock_messages.extend([user_message, agent_response])
        
        return agent_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send message: {str(e)}"
        )


@router.get("/chat/history", response_model=List[dict])
async def get_chat_history(skip: int = 0, limit: int = 100):
    """Get chat history."""
    return mock_messages[skip:skip + limit]


@router.delete("/chat/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history():
    """Clear chat history."""
    global mock_messages
    mock_messages = []
    return None