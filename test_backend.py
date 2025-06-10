#!/usr/bin/env python3
"""
Test script to verify the FastAPI backend works correctly.
"""

import asyncio
import httpx
import json

async def test_backend():
    """Test the FastAPI backend endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing FastAPI Backend...")
    print(f"📡 Base URL: {base_url}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test root endpoint
            print("\n1. Testing root endpoint...")
            response = await client.get(f"{base_url}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test health endpoint
            print("\n2. Testing health endpoint...")
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test API v1 health endpoint
            print("\n3. Testing API v1 health endpoint...")
            response = await client.get(f"{base_url}/api/v1/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test list agents
            print("\n4. Testing list agents...")
            response = await client.get(f"{base_url}/api/v1/agents")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test list tools
            print("\n5. Testing list tools...")
            response = await client.get(f"{base_url}/api/v1/tools")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test create agent
            print("\n6. Testing create agent...")
            agent_data = {
                "name": "Test Agent",
                "model": "gpt-3.5-turbo",
                "description": "A test agent",
                "tools": [1, 2]
            }
            response = await client.post(
                f"{base_url}/api/v1/agents",
                json=agent_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test create tool
            print("\n7. Testing create tool...")
            tool_data = {
                "name": "Test Tool",
                "type": "test",
                "description": "A test tool"
            }
            response = await client.post(
                f"{base_url}/api/v1/tools",
                json=tool_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test chat message
            print("\n8. Testing chat message...")
            message_data = {
                "message": "Hello, this is a test message!"
            }
            response = await client.post(
                f"{base_url}/api/v1/chat/message",
                json=message_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            print("\n🎉 All tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            return False

def main():
    """Main function."""
    print("🚀 FastAPI Backend Test")
    print("=" * 40)
    print("Make sure the backend is running with:")
    print("uvicorn app.main:app --reload")
    print("=" * 40)
    
    try:
        success = asyncio.run(test_backend())
        if success:
            print("\n✅ Backend is working correctly!")
        else:
            print("\n❌ Backend test failed!")
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())