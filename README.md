# FastAPI Agent Backend

A FastAPI-based backend service for AI agents using LangChain and Google Gemini integration.

## Project Structure

```
flash/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── agent.py    # Agent-related endpoints
│   │       │   ├── chat.py     # Chat endpoints
│   │       │   └── health.py   # Health check endpoints
│   │       └── api.py          # API router aggregation
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
│   │   ├── dependencies.py     # FastAPI dependencies
│   │   └── security.py         # Security utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent.py            # Agent data models
│   │   ├── chat.py             # Chat data models
│   │   └── common.py           # Common data models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py    # Agent business logic
│   │   ├── chat_service.py     # Chat business logic
│   │   └── llm_service.py      # LLM integration service
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging utilities
│       └── helpers.py          # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   └── test_services/
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── main.py                     # Application runner
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd flash
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FastAPI Agent Backend
DEBUG=True

# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### 5. Run the Application

#### Development Mode (with auto-reload):

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Production Mode:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## API Endpoints

### Health Check
- `GET /api/v1/health` - Application health status

### Agent Endpoints
- `POST /api/v1/agent/create` - Create a new agent
- `GET /api/v1/agent/{agent_id}` - Get agent details
- `PUT /api/v1/agent/{agent_id}` - Update agent
- `DELETE /api/v1/agent/{agent_id}` - Delete agent

### Chat Endpoints
- `POST /api/v1/chat/message` - Send a message to agent
- `GET /api/v1/chat/history/{session_id}` - Get chat history
- `POST /api/v1/chat/session` - Create new chat session

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

### Adding New Dependencies

```bash
# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_V1_STR` | API version prefix | `/api/v1` |
| `PROJECT_NAME` | Project name | `FastAPI Agent Backend` |
| `DEBUG` | Debug mode | `False` |
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **LangChain Integration**: Advanced language model capabilities
- **Google Gemini**: AI model integration
- **Async Support**: Asynchronous request handling
- **Auto Documentation**: Automatic API documentation generation
- **Modular Architecture**: Clean separation of concerns
- **Environment Configuration**: Flexible configuration management
- **Logging**: Comprehensive logging system
- **Testing**: Test framework setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

This project is licensed under the MIT License.