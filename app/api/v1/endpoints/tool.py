"""Tool-related endpoints."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models.tool import ToolCreate, ToolUpdate

router = APIRouter()

# Mock data for development
mock_tools = [
    {
        "id": 1,
        "name": "Web Search",
        "type": "search",
        "description": "Search the web for information",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "name": "Calculator",
        "type": "math",
        "description": "Perform mathematical calculations",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 3,
        "name": "File Reader",
        "type": "file",
        "description": "Read and analyze files",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
tool_counter = 4


@router.post("/tools", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_tool(tool_data: ToolCreate):
    """Create a new tool."""
    global tool_counter
    try:
        # Create mock tool
        tool_dict = {
            "id": tool_counter,
            "name": tool_data.name,
            "type": tool_data.type,
            "description": tool_data.description,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        mock_tools.append(tool_dict)
        tool_counter += 1
        return tool_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create tool: {str(e)}"
        )


@router.get("/tools/{tool_id}", response_model=dict)
async def get_tool(tool_id: int):
    """Get tool by ID."""
    tool = next((t for t in mock_tools if t["id"] == tool_id), None)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    return tool


@router.get("/tools", response_model=List[dict])
async def list_tools(skip: int = 0, limit: int = 100):
    """List all tools."""
    return mock_tools[skip:skip + limit]


@router.put("/tools/{tool_id}", response_model=dict)
async def update_tool(tool_id: int, tool_update: ToolUpdate):
    """Update a tool."""
    tool = next((t for t in mock_tools if t["id"] == tool_id), None)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    
    # Update tool fields
    if tool_update.name is not None:
        tool["name"] = tool_update.name
    if tool_update.type is not None:
        tool["type"] = tool_update.type
    if tool_update.description is not None:
        tool["description"] = tool_update.description
    
    tool["updated_at"] = "2024-01-01T00:00:00Z"
    return tool


@router.delete("/tools/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(tool_id: int):
    """Delete a tool."""
    global mock_tools
    tool = next((t for t in mock_tools if t["id"] == tool_id), None)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    
    mock_tools = [t for t in mock_tools if t["id"] != tool_id]
    return None