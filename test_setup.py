#!/usr/bin/env python3
"""
Test script to verify the cleaned up project structure works correctly.
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path.cwd()))
        
        # Test core imports
        from app.utils.api_client import get_api_client
        from app.utils.config import get_config
        from app.utils.error_handler import safe_async_call, LoadingState, show_success_message
        print("   ✅ Core utilities imported successfully")
        
        # Test component imports
        from app.components.agent_management import agent_management_section, load_agents
        from app.components.tool_management import tool_management_section, load_tools
        from app.components.chat_interface import chat_interface
        from app.components.system_monitoring import system_monitoring
        print("   ✅ UI components imported successfully")
        
        # Test instantiation
        api_client = get_api_client()
        config = get_config()
        print("   ✅ Objects instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_file_structure():
    """Test if required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app/__init__.py",
        "app/components/__init__.py",
        "app/components/agent_management.py",
        "app/components/tool_management.py", 
        "app/components/chat_interface.py",
        "app/components/system_monitoring.py",
        "app/utils/api_client.py",
        "app/utils/config.py",
        "app/utils/error_handler.py",
        "app/streamlit_app.py",
        "app/main.py",
        "launch.py",
        "main.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   ❌ {file_path}")
        return False
    
    print("   ✅ All required files found")
    return True

def main():
    """Main test function."""
    print("🧪 AI Agent Management Platform - Setup Test")
    print("=" * 50)
    
    all_good = True
    
    # Test file structure
    if not test_file_structure():
        all_good = False
    
    # Test imports
    if not test_imports():
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All tests passed! Your setup is ready.")
        print("💡 You can now run: python launch.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())