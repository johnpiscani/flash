"""Streamlit application for AI Agent Management - Simplified and Modular."""

import sys
from pathlib import Path
import streamlit as st
from app.utils.api_client import get_api_client
from app.utils.config import get_config
from app.utils.error_handler import safe_async_call, LoadingState
from app.components.agent_management import agent_management_section, load_agents
from app.components.tool_management import tool_management_section, load_tools
from app.components.chat_interface import chat_interface
from app.components.system_monitoring import system_monitoring


# Add the parent directory to Python path to enable imports
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))


config = get_config()
st.set_page_config(
    page_title=config.page_title,
    page_icon=config.page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_app():
    """Initialize the Streamlit application."""
    
    # Initialize API client
    return get_api_client(), config


def load_data(api_client):
    """Load agents and tools data."""
    # Initialize session states
    if 'agents_data' not in st.session_state:
        st.session_state.agents_data = []
    if 'tools_data' not in st.session_state:
        st.session_state.tools_data = []

    # Load data
    with LoadingState("Loading data..."):
        agents = safe_async_call(load_agents, api_client)
        tools = safe_async_call(load_tools, api_client)
        
        if agents is not None:
            st.session_state.agents_data = agents
        if tools is not None:
            st.session_state.tools_data = tools


def setup_sidebar(config, api_client):
    """Setup sidebar navigation and configuration."""
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Agent Management", "Tool Management", "Chat Interface", "System Monitoring"]
    )
    
    # API Configuration in sidebar
    with st.sidebar.expander("⚙️ API Configuration"):
        st.write(f"**API Base URL:** {config.api_base_url}")
        st.write(f"**Debug Mode:** {config.debug}")
        
        if st.button("Test Connection"):
            with LoadingState("Testing connection..."):
                try:
                    health_result = safe_async_call(api_client.health_check)
                    if health_result:
                        st.success("✅ Connection successful")
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")
    
    return page


def main():
    """Main Streamlit application."""
    # Initialize app
    api_client, config = initialize_app()
    
    # App title
    st.title("🤖 AI Agent Management Platform")
    
    # Load data
    load_data(api_client)
    
    # Setup sidebar and get selected page
    page = setup_sidebar(config, api_client)
    
    # Page routing
    if page == "Agent Management":
        agent_management_section(api_client, st.session_state.tools_data)
    elif page == "Tool Management":
        tool_management_section(api_client)
    elif page == "Chat Interface":
        chat_interface(api_client, st.session_state.agents_data)
    elif page == "System Monitoring":
        system_monitoring(api_client, st.session_state.agents_data, st.session_state.tools_data)


if __name__ == "__main__":
    main()