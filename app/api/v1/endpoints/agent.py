"""Agent-related endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models.agent import Agent, AgentCreate, AgentUpdate
from app.services.agent_service import AgentService

router = APIRouter()

# Mock data for development
mock_agents = []
agent_counter = 1


@router.post("/agents", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_agent(agent_data: AgentCreate):
    """Create a new agent."""
    global agent_counter
    try:
        # Create mock agent
        agent_dict = {
            "id": agent_counter,
            "name": agent_data.name,
            "model": agent_data.model,
            "description": agent_data.description,
            "tools": agent_data.tools or [],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        mock_agents.append(agent_dict)
        agent_counter += 1
        return agent_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.get("/agents/{agent_id}", response_model=dict)
async def get_agent(agent_id: int):
    """Get agent by ID."""
    agent = next((a for a in mock_agents if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.get("/agents", response_model=List[dict])
async def list_agents(skip: int = 0, limit: int = 100):
    """List all agents."""
    return mock_agents[skip:skip + limit]


@router.put("/agents/{agent_id}", response_model=dict)
async def update_agent(agent_id: int, agent_update: AgentUpdate):
    """Update an agent."""
    agent = next((a for a in mock_agents if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Update agent fields
    if agent_update.name is not None:
        agent["name"] = agent_update.name
    if agent_update.model is not None:
        agent["model"] = agent_update.model
    if agent_update.description is not None:
        agent["description"] = agent_update.description
    if agent_update.tools is not None:
        agent["tools"] = agent_update.tools
    
    agent["updated_at"] = "2024-01-01T00:00:00Z"
    return agent


@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: int):
    """Delete an agent."""
    global mock_agents
    agent = next((a for a in mock_agents if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    mock_agents = [a for a in mock_agents if a["id"] != agent_id]
    return None