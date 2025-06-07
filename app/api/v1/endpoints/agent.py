"""Agent-related endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.agent import Agent, AgentCreate, AgentUpdate
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/agent", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: dict = Depends(get_current_user),
    agent_service: AgentService = Depends(AgentService)
):
    """Create a new agent."""
    try:
        agent = await agent_service.create_agent(agent_data, current_user["user_id"])
        return agent
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.get("/agent/{agent_id}", response_model=Agent)
async def get_agent(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user),
    agent_service: AgentService = Depends(AgentService)
):
    """Get agent by ID."""
    agent = await agent_service.get_agent(agent_id, current_user["user_id"])
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.get("/agents", response_model=List[Agent])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    agent_service: AgentService = Depends(AgentService)
):
    """List all agents for the current user."""
    agents = await agent_service.list_agents(
        current_user["user_id"], 
        skip=skip, 
        limit=limit
    )
    return agents


@router.put("/agent/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: UUID,
    agent_update: AgentUpdate,
    current_user: dict = Depends(get_current_user),
    agent_service: AgentService = Depends(AgentService)
):
    """Update an agent."""
    agent = await agent_service.update_agent(
        agent_id, 
        agent_update, 
        current_user["user_id"]
    )
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.delete("/agent/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user),
    agent_service: AgentService = Depends(AgentService)
):
    """Delete an agent."""
    success = await agent_service.delete_agent(agent_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )