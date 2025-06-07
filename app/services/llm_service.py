"""LLM service for handling language model interactions."""

import time
from typing import Dict, List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

from app.core.config import settings
from app.models.agent import Agent
from app.models.chat import ChatMessage, MessageRole


class LLMService:
    """Service for handling LLM interactions."""
    
    def __init__(self):
        """Initialize LLM service."""
        self.llm = None
        if settings.GOOGLE_API_KEY:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7
            )
    
    async def generate_response(
        self,
        agent: Agent,
        message: str,
        chat_history: List[ChatMessage] = None
    ) -> Dict:
        """Generate response using the LLM."""
        if not self.llm:
            raise ValueError("LLM not configured. Please set GOOGLE_API_KEY.")
        
        start_time = time.time()
        
        try:
            # Prepare messages
            messages = []
            
            # Add system message
            if agent.system_prompt:
                messages.append(SystemMessage(content=agent.system_prompt))
            
            # Add chat history
            if chat_history:
                for msg in chat_history[-10:]:  # Last 10 messages for context
                    if msg.role == MessageRole.USER:
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == MessageRole.ASSISTANT:
                        messages.append(SystemMessage(content=f"Assistant: {msg.content}"))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Configure LLM with agent settings
            self.llm.temperature = agent.temperature
            if agent.max_tokens:
                self.llm.max_output_tokens = agent.max_tokens
            
            # Generate response
            response = await self.llm.ainvoke(messages)
            
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "content": response.content,
                "response_time_ms": response_time,
                "token_count": len(response.content.split()),  # Rough estimate
                "model": agent.model_name
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate LLM response: {str(e)}")
    
    async def validate_agent_config(self, agent: Agent) -> bool:
        """Validate agent configuration with LLM."""
        try:
            test_message = "Hello, this is a test message."
            response = await self.generate_response(agent, test_message)
            return bool(response.get("content"))
        except Exception:
            return False