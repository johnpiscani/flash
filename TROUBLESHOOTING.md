# 🔧 Troubleshooting Guide

## Quick Fixes

### 1. **Backend Won't Start**
**Error**: Issues when running `uvicorn app.main:app --reload`

**Solutions**:
```bash
# Option A: Run from project root
cd /path/to/your/project
uvicorn app.main:app --reload

# Option B: Use the test script first
python test_backend.py

# Option C: Check for import errors
python -c "from app.main import app; print('✅ Backend imports OK')"
```

### 2. **Streamlit Import Errors**
**Error**: `ModuleNotFoundError: No module named 'app.utils.api_client'`

**Solutions**:
```bash
# Option A: Use the launcher (Recommended)
python launch_streamlit.py

# Option B: Run debug script first
python debug_setup.py

# Option C: Set PYTHONPATH manually
export PYTHONPATH=$PWD:$PYTHONPATH
streamlit run app/streamlit_app.py
```

### 3. **Connection Errors**
**Error**: "Connection Error: Unable to connect to the API server"

**Solutions**:
1. **Start backend first**: `uvicorn app.main:app --reload`
2. **Wait for backend**: Backend needs ~5 seconds to start
3. **Check ports**: Backend on 8000, Frontend on 8501
4. **Test connection**: `python test_backend.py`

## Step-by-Step Debugging

### Step 1: Verify File Structure
```bash
python debug_setup.py
```
This checks:
- ✅ All required files exist
- ✅ Python path is correct
- ✅ Dependencies are installed
- ✅ Imports work correctly

### Step 2: Test Backend Separately
```bash
# Start backend
uvicorn app.main:app --reload

# In another terminal, test it
python test_backend.py
```

### Step 3: Test Frontend Separately
```bash
# Make sure backend is running first
python launch_streamlit.py
```

### Step 4: Run Both Together
```bash
python run_app.py
```

## Common Error Messages

### Backend Errors

#### "ModuleNotFoundError: No module named 'app.api.v1.api'"
**Cause**: Missing files or incorrect imports
**Fix**: 
```bash
# Check if files exist
ls app/api/v1/
# Should show: __init__.py, api.py, endpoints/

# If missing, the backend has been simplified to work without complex dependencies
```

#### "ImportError: cannot import name 'get_current_user'"
**Cause**: Authentication dependencies issue
**Fix**: The endpoints have been simplified to work without authentication

### Frontend Errors

#### "Import Error: No module named 'app.utils.api_client'"
**Cause**: Python path not set correctly
**Fix**: 
```bash
python launch_streamlit.py  # This sets the path correctly
```

#### "Connection Error: Unable to connect to the API server"
**Cause**: Backend not running or wrong URL
**Fix**:
1. Start backend: `uvicorn app.main:app --reload`
2. Wait 5 seconds
3. Test: `curl http://localhost:8000/health`

## Testing Commands

### Test Everything
```bash
# 1. Debug setup
python debug_setup.py

# 2. Test backend
python test_backend.py

# 3. Test frontend imports
python test_streamlit.py

# 4. Run application
python run_app.py
```

### Individual Component Tests
```bash
# Test just imports
python test_imports.py

# Test just backend
uvicorn app.main:app --reload
# Then: python test_backend.py

# Test just frontend
python launch_streamlit.py
```

## Environment Setup

### Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# (Currently no API keys required for basic functionality)
```

## Port Configuration

### Default Ports
- **Backend (FastAPI)**: http://localhost:8000
- **Frontend (Streamlit)**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

### Change Ports
```bash
# Backend on different port
uvicorn app.main:app --reload --port 8080

# Frontend on different port
streamlit run app/streamlit_app.py --server.port 8502
```

## Development vs Production

### Development Mode (Current)
- Uses mock data
- No authentication required
- Auto-reload enabled
- CORS allows all origins

### Production Setup (Future)
- Real database integration
- Authentication enabled
- Environment-specific configuration
- Proper CORS configuration

## Getting Help

### Check Logs
```bash
# Backend logs
uvicorn app.main:app --reload --log-level debug

# Frontend logs
streamlit run app/streamlit_app.py --logger.level debug
```

### Verify Installation
```bash
# Check Python version (should be 3.8+)
python --version

# Check installed packages
pip list | grep -E "(streamlit|fastapi|uvicorn|httpx)"

# Check if ports are available
netstat -an | grep -E "(8000|8501)"
```

### Reset Everything
```bash
# Stop all processes
pkill -f "uvicorn\|streamlit"

# Clear Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Restart
python run_app.py
```

## Success Indicators

### Backend Working ✅
- `uvicorn app.main:app --reload` starts without errors
- `http://localhost:8000` shows welcome message
- `http://localhost:8000/docs` shows API documentation
- `python test_backend.py` passes all tests

### Frontend Working ✅
- `python launch_streamlit.py` starts without errors
- `http://localhost:8501` shows the Streamlit interface
- Can navigate between pages (Agents, Tools, Chat, Monitoring)
- No import errors in the browser console

### Integration Working ✅
- Frontend can connect to backend
- Can create/edit/delete agents and tools
- Chat interface responds (with mock responses)
- System monitoring shows healthy status

---

**Still having issues?** 
1. Run `python debug_setup.py` for comprehensive diagnostics
2. Check that you're in the project root directory
3. Ensure all requirements are installed: `pip install -r requirements.txt`
4. Try the individual test scripts to isolate the problem