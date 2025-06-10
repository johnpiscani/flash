"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import agent, chat, health, tool

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(agent.router, tags=["agents"])
api_router.include_router(tool.router, tags=["tools"])
api_router.include_router(chat.router, tags=["chat"])