#!/usr/bin/env python3
"""
Simple launcher for the AI Agent Management Platform.
Starts both FastAPI backend and Streamlit frontend.
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path


def check_requirements():
    """Check if basic requirements are met."""
    print("📋 Checking requirements...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("⚠️  Warning: .env file not found. Copy .env.example to .env and configure it.")
    
    # Check basic imports
    try:
        import streamlit
        import fastapi
        import httpx
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False


def run_fastapi():
    """Run FastAPI backend server."""
    print("🚀 Starting FastAPI backend...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ FastAPI server stopped")
    except Exception as e:
        print(f"❌ Error running FastAPI: {e}")


def run_streamlit():
    """Run Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    time.sleep(3)  # Wait for FastAPI to start
    
    # Set up environment
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path.cwd())
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], env=env, check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Streamlit server stopped")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")


def main():
    """Main function to launch the application."""
    print("🤖 AI Agent Management Platform")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed. Please install dependencies first.")
        return 1
    
    print("🚀 Starting both FastAPI backend and Streamlit frontend...")
    print("📍 FastAPI will be available at: http://localhost:8000")
    print("📍 Streamlit will be available at: http://localhost:8501")
    print("=" * 50)
    
    # Start both servers in separate threads
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    
    try:
        fastapi_thread.start()
        streamlit_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        return 0


if __name__ == "__main__":
    sys.exit(main())