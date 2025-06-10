"""Tool service for managing tools."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.tool import Tool, ToolCreate, ToolUpdate


class ToolService:
    """Service for managing tools."""
    
    def __init__(self):
        """Initialize tool service."""
        # In a real application, you would inject a database service here
        self._tools_storage = {}  # Temporary in-memory storage
        
        # Initialize with some default tools
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """Initialize with some default tools."""
        default_tools = [
            {
                "name": "Web Search",
                "description": "Search the web for information",
                "tool_type": "API Integration",
                "category": "Data",
                "user_id": "default_user"
            },
            {
                "name": "File Reader",
                "description": "Read and process various file formats",
                "tool_type": "File Handler",
                "category": "Utility",
                "user_id": "default_user"
            },
            {
                "name": "Calculator",
                "description": "Perform mathematical calculations",
                "tool_type": "Calculator",
                "category": "Utility",
                "user_id": "default_user"
            },
            {
                "name": "Email Sender",
                "description": "Send emails to recipients",
                "tool_type": "Communication",
                "category": "Communication",
                "user_id": "default_user"
            },
            {
                "name": "Data Analyzer",
                "description": "Analyze and process data",
                "tool_type": "Data Processing",
                "category": "Analysis",
                "user_id": "default_user"
            }
        ]
        
        for tool_data in default_tools:
            tool = Tool(**tool_data)
            self._tools_storage[str(tool.id)] = tool
    
    async def create_tool(self, tool_data: ToolCreate, user_id: str) -> Tool:
        """Create a new tool."""
        tool = Tool(
            **tool_data.dict(),
            user_id=user_id
        )
        
        # Store tool (in real app, this would be in a database)
        self._tools_storage[str(tool.id)] = tool
        
        return tool
    
    async def get_tool(self, tool_id: UUID, user_id: str) -> Optional[Tool]:
        """Get tool by ID."""
        tool = self._tools_storage.get(str(tool_id))
        if tool and tool.user_id == user_id:
            return tool
        return None
    
    async def list_tools(
        self, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Tool]:
        """List all tools for a user."""
        user_tools = [
            tool for tool in self._tools_storage.values()
            if tool.user_id == user_id and tool.is_active
        ]
        return user_tools[skip:skip + limit]
    
    async def update_tool(
        self, 
        tool_id: UUID, 
        tool_update: ToolUpdate, 
        user_id: str
    ) -> Optional[Tool]:
        """Update a tool."""
        tool = await self.get_tool(tool_id, user_id)
        if not tool:
            return None
        
        # Update fields
        update_data = tool_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tool, field, value)
        
        tool.updated_at = datetime.utcnow()
        
        # Store updated tool
        self._tools_storage[str(tool.id)] = tool
        
        return tool
    
    async def delete_tool(self, tool_id: UUID, user_id: str) -> bool:
        """Delete a tool."""
        tool = await self.get_tool(tool_id, user_id)
        if not tool:
            return False
        
        # Soft delete
        tool.is_active = False
        tool.updated_at = datetime.utcnow()
        
        return True