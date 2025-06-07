# FastAPI Agent Backend - Project Overview

## Architecture

This FastAPI application follows a clean architecture pattern with clear separation of concerns:

### Directory Structure
```
flash/
├── app/                    # Main application package
│   ├── api/               # API layer
│   │   └── v1/           # API version 1
│   │       ├── endpoints/ # Individual endpoint modules
│   │       └── api.py    # Router aggregation
│   ├── core/             # Core application logic
│   │   ├── config.py     # Configuration management
│   │   └── dependencies.py # FastAPI dependencies
│   ├── models/           # Data models (Pydantic)
│   │   ├── agent.py      # Agent models
│   │   ├── chat.py       # Chat models
│   │   └── common.py     # Common models
│   ├── services/         # Business logic layer
│   │   ├── agent_service.py # Agent management
│   │   ├── chat_service.py  # Chat management
│   │   └── llm_service.py   # LLM integration
│   └── utils/            # Utility functions
│       ├── logger.py     # Logging utilities
│       └── helpers.py    # Helper functions
├── tests/                # Test modules
└── main.py              # Application entry point
```

## Key Features

### 1. Agent Management
- Create, read, update, delete AI agents
- Configure agent parameters (temperature, max tokens, system prompts)
- Support for different LLM models
- Agent validation and testing

### 2. Chat System
- Create chat sessions with specific agents
- Send messages and receive AI responses
- Chat history management
- Session management

### 3. LLM Integration
- Google Gemini integration via LangChain
- Configurable model parameters
- Response time tracking
- Token usage estimation

### 4. API Design
- RESTful API design
- Automatic OpenAPI documentation
- Versioned API endpoints
- Comprehensive error handling

## Technology Stack

- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and serialization
- **LangChain**: LLM integration framework
- **Google Gemini**: AI language model
- **Uvicorn**: ASGI server
- **Python 3.8+**: Programming language

## Data Flow

1. **Request**: Client sends HTTP request to API endpoint
2. **Validation**: Pydantic models validate request data
3. **Authentication**: Dependencies verify user access
4. **Service Layer**: Business logic processes the request
5. **LLM Integration**: If needed, service calls LLM via LangChain
6. **Response**: Formatted response returned to client

## Configuration

The application uses environment variables for configuration:

- `GOOGLE_API_KEY`: Required for Gemini integration
- `DEBUG`: Enable/disable debug mode
- `HOST`/`PORT`: Server configuration
- `LOG_LEVEL`: Logging verbosity

## Development Workflow

1. **Setup**: Run `./setup.sh` to create environment and install dependencies
2. **Configure**: Edit `.env` file with your settings
3. **Run**: Execute `./start.sh` or `python main.py`
4. **Test**: Access API docs at `http://localhost:8000/docs`
5. **Develop**: Make changes and restart (auto-reload in debug mode)

## API Endpoints

### Health
- `GET /health` - Basic health check
- `GET /api/v1/health` - API health check
- `GET /api/v1/health/detailed` - Detailed health check

### Agents
- `POST /api/v1/agent` - Create agent
- `GET /api/v1/agent/{id}` - Get agent
- `GET /api/v1/agents` - List agents
- `PUT /api/v1/agent/{id}` - Update agent
- `DELETE /api/v1/agent/{id}` - Delete agent

### Chat
- `POST /api/v1/chat/session` - Create chat session
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/history/{session_id}` - Get chat history
- `GET /api/v1/chat/sessions` - List sessions
- `DELETE /api/v1/chat/session/{id}` - Delete session

## Security Considerations

- API key authentication (placeholder implementation)
- User isolation (agents and chats are user-specific)
- Input validation via Pydantic models
- CORS configuration for web clients

## Scalability Notes

- In-memory storage (replace with database for production)
- Stateless design for horizontal scaling
- Async/await for concurrent request handling
- Modular architecture for easy extension

## Next Steps for Production

1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Authentication**: Implement proper JWT/OAuth authentication
3. **Caching**: Add Redis for session and response caching
4. **Monitoring**: Add logging, metrics, and health checks
5. **Deployment**: Containerize with Docker and deploy to cloud
6. **Testing**: Expand test coverage and add integration tests