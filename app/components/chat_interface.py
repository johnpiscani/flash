"""Chat interface UI component."""

import streamlit as st
from typing import Dict, List, Optional

from app.utils.error_handler import safe_async_call, LoadingState


def display_agent_info(agent_data: Dict):
    """Display agent information in an expandable section."""
    with st.expander("Agent Information", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Model:** {agent_data.get('model_name', 'N/A')}")
            st.write(f"**Temperature:** {agent_data.get('temperature', 'N/A')}")
        with col2:
            tools = agent_data.get('tools', [])
            st.write(f"**Tools:** {', '.join(tools) if tools else 'None'}")
        
        st.write(f"**System Prompt:** {agent_data.get('system_prompt', 'N/A')}")


def display_chat_history(chat_history: List[Dict]):
    """Display chat history messages."""
    for message in chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['message'])
        else:
            st.chat_message("assistant").write(message['message'])


def chat_interface(api_client, agents_data: List[Dict]):
    """Main chat interface section."""
    st.header("💬 Agent Chat")

    if not agents_data:
        st.info("No agents available. Please create an agent first to start chatting.")
        return

    # Agent selection
    agent_names = [agent['name'] for agent in agents_data]
    selected_agent = st.selectbox("Choose an Agent", agent_names)
    
    # Find selected agent details
    selected_agent_data = next(
        (agent for agent in agents_data if agent['name'] == selected_agent), 
        None
    )
    
    if not selected_agent_data:
        st.error("Selected agent not found.")
        return

    # Display agent info
    display_agent_info(selected_agent_data)

    st.subheader("Chat History")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    display_chat_history(st.session_state.chat_history)

    # Chat input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.chat_message("user").write(user_input)
        
        # Simulate AI response (replace with actual API call)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # TODO: Implement actual chat API call
                response = f"I'm {selected_agent}, and I received your message: '{user_input}'. This is a placeholder response. Actual chat functionality will be implemented with the chat API."
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "message": response})