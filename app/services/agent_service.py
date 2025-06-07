"""Agent service for managing AI agents."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.agent import Agent, AgentCreate, AgentUpdate
from app.services.llm_service import LLMService


class AgentService:
    """Service for managing agents."""
    
    def __init__(self):
        """Initialize agent service."""
        self.llm_service = LLMService()
        # In a real application, you would inject a database service here
        self._agents_storage = {}  # Temporary in-memory storage
    
    async def create_agent(self, agent_data: AgentCreate, user_id: str) -> Agent:
        """Create a new agent."""
        agent = Agent(
            **agent_data.dict(),
            user_id=user_id
        )
        
        # Validate agent configuration
        is_valid = await self.llm_service.validate_agent_config(agent)
        if not is_valid:
            raise ValueError("Invalid agent configuration")
        
        # Store agent (in real app, this would be in a database)
        self._agents_storage[str(agent.id)] = agent
        
        return agent
    
    async def get_agent(self, agent_id: UUID, user_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        agent = self._agents_storage.get(str(agent_id))
        if agent and agent.user_id == user_id:
            return agent
        return None
    
    async def list_agents(
        self, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Agent]:
        """List all agents for a user."""
        user_agents = [
            agent for agent in self._agents_storage.values()
            if agent.user_id == user_id and agent.is_active
        ]
        return user_agents[skip:skip + limit]
    
    async def update_agent(
        self, 
        agent_id: UUID, 
        agent_update: AgentUpdate, 
        user_id: str
    ) -> Optional[Agent]:
        """Update an agent."""
        agent = await self.get_agent(agent_id, user_id)
        if not agent:
            return None
        
        # Update fields
        update_data = agent_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        agent.updated_at = datetime.utcnow()
        
        # Validate updated configuration
        is_valid = await self.llm_service.validate_agent_config(agent)
        if not is_valid:
            raise ValueError("Invalid agent configuration after update")
        
        # Store updated agent
        self._agents_storage[str(agent.id)] = agent
        
        return agent
    
    async def delete_agent(self, agent_id: UUID, user_id: str) -> bool:
        """Delete an agent."""
        agent = await self.get_agent(agent_id, user_id)
        if not agent:
            return False
        
        # Soft delete
        agent.is_active = False
        agent.updated_at = datetime.utcnow()
        
        return True