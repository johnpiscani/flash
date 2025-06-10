"""API client for Streamlit to communicate with FastAPI backend."""

import json
from typing import Dict, List, Optional, Any
from uuid import UUID
import httpx
import streamlit as st


class APIClient:
    """Client for communicating with FastAPI backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        """Initialize API client."""
        self.base_url = base_url.rstrip("/")
        self.api_v1_url = f"{self.base_url}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.api_v1_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                if method.upper() == "GET":
                    response = await client.get(url, headers=self.headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=self.headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                
                # Handle empty responses (like DELETE)
                if response.status_code == 204:
                    return {"success": True}
                
                return response.json()
                
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_response = e.response.json()
                error_detail = error_response.get("detail", str(e))
            except:
                error_detail = str(e)
            
            raise Exception(f"API Error ({e.response.status_code}): {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Connection Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")
    
    # Agent endpoints
    async def create_agent(self, agent_data: Dict) -> Dict:
        """Create a new agent."""
        return await self._make_request("POST", "/agents", data=agent_data)
    
    async def get_agent(self, agent_id: str) -> Dict:
        """Get agent by ID."""
        return await self._make_request("GET", f"/agents/{agent_id}")
    
    async def list_agents(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all agents."""
        params = {"skip": skip, "limit": limit}
        return await self._make_request("GET", "/agents", params=params)
    
    async def update_agent(self, agent_id: str, agent_data: Dict) -> Dict:
        """Update an agent."""
        return await self._make_request("PUT", f"/agents/{agent_id}", data=agent_data)
    
    async def delete_agent(self, agent_id: str) -> Dict:
        """Delete an agent."""
        return await self._make_request("DELETE", f"/agents/{agent_id}")
    
    # Tool endpoints
    async def create_tool(self, tool_data: Dict) -> Dict:
        """Create a new tool."""
        return await self._make_request("POST", "/tools", data=tool_data)
    
    async def get_tool(self, tool_id: str) -> Dict:
        """Get tool by ID."""
        return await self._make_request("GET", f"/tools/{tool_id}")
    
    async def list_tools(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all tools."""
        params = {"skip": skip, "limit": limit}
        return await self._make_request("GET", "/tools", params=params)
    
    async def update_tool(self, tool_id: str, tool_data: Dict) -> Dict:
        """Update a tool."""
        return await self._make_request("PUT", f"/tools/{tool_id}", data=tool_data)
    
    async def delete_tool(self, tool_id: str) -> Dict:
        """Delete a tool."""
        return await self._make_request("DELETE", f"/tools/{tool_id}")
    
    # Chat endpoints
    async def send_message(self, message_data: Dict) -> Dict:
        """Send a chat message."""
        return await self._make_request("POST", "/chat/message", data=message_data)
    
    async def get_chat_history(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get chat history."""
        params = {"skip": skip, "limit": limit}
        return await self._make_request("GET", "/chat/history", params=params)
    
    async def clear_chat_history(self) -> Dict:
        """Clear chat history."""
        return await self._make_request("DELETE", "/chat/history")
    
    # Health check
    async def health_check(self) -> Dict:
        """Check API health."""
        return await self._make_request("GET", "/health")


# Singleton instance for Streamlit
@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance."""
    # You can configure these via environment variables or Streamlit secrets
    # base_url = st.secrets.get("API_BASE_URL", "http://localhost:8000")
    base_url = "http://localhost:8000"
    # api_key = st.secrets.get("API_KEY", None)
    api_key = None
    
    return APIClient(base_url=base_url, api_key=api_key)