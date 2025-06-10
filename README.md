# FastAPI Agent Backend

A comprehensive FastAPI-based backend service for AI agents and tools management, featuring a modern Streamlit UI and leveraging LangChain with Google Gemini integration.

## 🚀 Features

### 🎨 Modern Web Interface
- **Streamlit UI**: Clean, responsive web interface with navigation
- **Agent Management**: Create, edit, and manage AI agents with tool associations
- **Tool Management**: Comprehensive tool creation and management system
- **Chat Interface**: Real-time conversations with AI agents
- **System Monitoring**: Health and performance monitoring dashboard
- **Modal Workflows**: User-friendly creation and editing forms

### 🤖 Agent & Tool Management
- **Agent CRUD**: Full create, read, update, delete operations for agents
- **Tool Integration**: Assign multiple tools to agents during creation/editing
- **Interactive Tables**: Easy-to-use data visualization and management
- **Template System**: Planned template-based creation for rapid deployment

### 💬 Chat System
- Real-time conversations with AI agents
- Agent selection for targeted conversations
- Chat history and session management
- Context-aware responses with tool integration

### 🔧 LLM Integration
- Google Gemini API integration via LangChain
- Configurable model parameters (temperature, max tokens)
- Tool-enhanced agent responses
- Error handling and fallback mechanisms

## 🏗️ Project Structure

```
flash/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── streamlit_app.py        # Streamlit UI application
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
│       ├── helpers.py          # Helper functions
│       └── logger.py           # Logging utilities
├── TODO.md                     # Development roadmap and tasks
├── PROJECT_OVERVIEW.md         # Detailed project documentation
├── .env.example               # Environment variables template
└── requirements.txt           # Python dependencies
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based web UI)
- **Backend**: FastAPI (Modern, fast web framework)
- **LLM Integration**: LangChain + Google Gemini
- **Data Validation**: Pydantic models
- **Async Support**: Full asynchronous request handling
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Configuration**: Environment variable-based configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flash
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

### Running the Application

#### Streamlit UI (Frontend)
```bash
streamlit run app/streamlit_app.py
```
Access the UI at: `http://localhost:8501`

#### FastAPI Backend
```bash
python app/main.py
# or
uvicorn app.main:app --reload
```
Access the API at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### Full Stack Development
Run both applications simultaneously for complete development experience.

## 📖 Usage

### Agent Management
1. Navigate to "Agent Management" in the sidebar
2. Click "Create New Agent" to add a new agent
3. Select tools to associate with the agent
4. Use the interactive table to edit or delete existing agents

### Tool Management
1. Navigate to "Tool Management" in the sidebar
2. Create new tools with specific types and categories
3. Manage existing tools through the interactive interface

### Chat Interface
1. Go to "Chat Interface" in the sidebar
2. Select an agent from the dropdown
3. Start chatting with your AI agent
4. View chat history and manage conversations

### System Monitoring
1. Check "System Monitoring" for health status
2. View API performance metrics
3. Monitor recent API calls and system resources

## 🔧 API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /api/v1/health` - API health check

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

## 🔄 Development Status

### ✅ Completed
- Complete Streamlit UI with navigation and multiple pages
- Agent management with tool association
- Tool management interface
- Interactive tables with edit/delete functionality
- Modal-based creation workflows
- Chat interface with agent selection
- System monitoring dashboard
- Basic FastAPI backend structure

### 🚧 In Progress
- API-UI integration for real-time data synchronization
- Database integration for persistent storage
- Prompt generation system

### 📋 Planned (See TODO.md)
- Complete backend API integration
- Database storage system (MongoDB/PostgreSQL)
- Advanced prompt generator with templates
- File and code association system
- Template system for rapid deployment
- Enhanced security and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Development Roadmap

See `TODO.md` for a comprehensive list of planned features and improvements, including:
- Database integration
- API-UI connection
- Prompt generation system
- Template system
- Enhanced security
- Production deployment

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Note**: This project is actively under development. See `PROJECT_OVERVIEW.md` for detailed architecture information and `TODO.md` for the development roadmap.ta models
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
│   └── app/
│       └── streamlit_app.py      # Streamlit UI Prototype
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
### Streamlit UI Prototype

A simple Streamlit-based UI prototype is available for quick interaction with the backend.

#### Running the Streamlit UI

```bash
# Ensure Streamlit is installed
pip install streamlit

# Run the Streamlit app
streamlit run app/streamlit_app.py
```

The Streamlit UI provides a basic interface for exploring agents and interacting with the backend. It serves as a lightweight frontend prototype before potential migration to more advanced frameworks like React or Angular.
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
