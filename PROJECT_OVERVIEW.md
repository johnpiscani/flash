# FastAPI Agent Backend - Project Overview

## Architecture Overview

This FastAPI application serves as a comprehensive backend for AI agent and tool management, featuring a modern Streamlit UI and leveraging LangChain for seamless integration with Large Language Models (LLMs), specifically Google Gemini. The architecture follows a modular, scalable design pattern that promotes separation of concerns and maintainability.

## Directory Structure
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
│   ├── streamlit_app.py  # Streamlit UI application
│   └── utils/            # Utility functions
│       ├── logger.py     # Logging utilities
│       └── helpers.py    # Helper functions
├── tests/                # Test modules
├── TODO.md              # Development roadmap and tasks
└── main.py              # Application entry point
```

## Key Features

### 🎨 Modern UI Interface
- **Streamlit-based Web UI**: Clean, responsive interface with navigation
- **Agent Management**: Create agents with tool selection, edit existing agents
- **Tool Management**: Comprehensive tool creation and management interface
- **Modal Workflows**: User-friendly creation and editing forms
- **Interactive Tables**: Easy-to-use data visualization and management
- **Chat Interface**: Real-time chat functionality with agents
- **System Monitoring**: Health and performance monitoring dashboard

### 🤖 Enhanced Agent Management
- Create, read, update, delete AI agents with full UI support
- **Tool Association**: Assign multiple tools to agents during creation/editing
- Configure agent parameters (temperature, max tokens, system prompts)
- Agent-specific prompt templates and behaviors
- Interactive table view with edit/delete functionality
- Modal-based creation and editing workflows

### 🛠️ Tool Management System
- Create and manage various tool types (API Integration, File Handler, Calculator, etc.)
- Tool categorization and organization (Utility, Data, Communication, Analysis)
- Interactive tool management interface
- Template-based tool creation (planned)
- Code snippet association with tools (planned)

### 💬 Chat System
- Create chat sessions with specific agents
- Agent selection for targeted conversations
- Send messages and receive AI responses
- Chat history management and session tracking
- Real-time conversation interface

### 🔧 LLM Integration
- Google Gemini integration via LangChain
- Configurable model parameters
- Response time tracking and token usage estimation
- Tool-enhanced agent responses
- Error handling and fallback mechanisms

### 📊 Monitoring & Health
- System health checks with visual indicators
- Performance metrics (CPU, Memory usage)
- API usage tracking and recent calls display
- Real-time status monitoring dashboard

## Technology Stack

- **Frontend**: Streamlit (Python-based web UI)
- **Backend**: FastAPI (Modern, fast web framework)
- **Data Validation**: Pydantic models for type safety
- **LLM Integration**: LangChain + Google Gemini
- **Server**: Uvicorn ASGI server
- **Python**: 3.8+ with async/await support

## Current Development Status

### ✅ Completed Features
- Complete Streamlit UI with navigation and multiple pages
- Agent management UI with table view and modal forms
- Tool management UI with creation and editing capabilities
- Agent-tool association during creation and editing
- Interactive agent and tool tables with functional edit/delete buttons
- Modal-based creation workflows for improved UX
- Chat interface with agent selection
- System monitoring dashboard
- Basic FastAPI backend structure

### 🚧 In Progress (See TODO.md)
- API-UI integration for real-time data synchronization
- Database integration for persistent storage
- Prompt generation system
- File and code association with tools/agents

### 📋 Planned Features
- Complete API backend integration with UI
- Database storage system (MongoDB/PostgreSQL evaluation)
- Advanced prompt generator with template system
- Code snippet and file association system
- Template system for rapid agent/tool deployment
- Enhanced security and authentication
- Production deployment configuration

## Data Flow

1. **UI Interaction**: User interacts with Streamlit interface
2. **State Management**: Session state manages UI modals and forms
3. **API Communication**: UI communicates with FastAPI backend (planned)
4. **Validation**: Pydantic models validate all data
5. **Service Layer**: Business logic processes requests
6. **LLM Integration**: Services call LLM via LangChain when needed
7. **Storage**: Data persisted to database (planned)
8. **Response**: Results displayed in UI with real-time updates

## Configuration

The application uses environment variables for configuration:

- `GOOGLE_API_KEY`: Required for Gemini integration
- `DEBUG`: Enable/disable debug mode
- `HOST`/`PORT`: Server configuration
- `LOG_LEVEL`: Logging verbosity

## Development Workflow

1. **Setup**: Run `./setup.sh` to create environment and install dependencies
2. **Configure**: Edit `.env` file with your settings
3. **UI Development**: Run `streamlit run app/streamlit_app.py` for frontend
4. **API Development**: Run `python main.py` for backend
5. **Test**: Access API docs at `http://localhost:8000/docs`
6. **Develop**: Make changes with auto-reload in debug mode

## API Endpoints (Backend)

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

### Tools (Planned)
- `POST /api/v1/tool` - Create tool
- `GET /api/v1/tool/{id}` - Get tool
- `GET /api/v1/tools` - List tools
- `PUT /api/v1/tool/{id}` - Update tool
- `DELETE /api/v1/tool/{id}` - Delete tool

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
- Secure session state management in UI

## Scalability Notes

- Modular UI architecture for easy component scaling
- Stateless backend design for horizontal scaling
- Async/await for concurrent request handling
- Database-ready architecture for data persistence
- Separation of UI and API for independent scaling

## Next Development Phase

The project is transitioning from UI prototype to full-stack application:

1. **Database Integration**: Implementing persistent storage for agents and tools
2. **API Connection**: Connecting Streamlit UI to FastAPI backend
3. **Prompt Engineering**: Building advanced prompt generation capabilities
4. **File Management**: Associating code snippets and files with tools/agents
5. **Template System**: Creating reusable templates for rapid deployment
6. **Production Readiness**: Authentication, monitoring, and deployment

## Getting Started

### For UI Development
```bash
streamlit run app/streamlit_app.py
```

### For API Development
```bash
python main.py
# or
uvicorn app.main:app --reload
```

### Full Stack Development
Run both UI and API simultaneously for complete development experience.

This architecture provides a solid foundation for building sophisticated AI agent systems with modern UI/UX while maintaining flexibility for future enhancements and scaling requirements. See `TODO.md` for detailed development roadmap and task tracking.
