"""Agent management UI component."""

import streamlit as st
from typing import Dict, List, Optional

from app.utils.error_handler import safe_async_call, LoadingState, show_success_message


async def load_agents(api_client) -> Optional[List[Dict]]:
    """Load agents from API."""
    return await api_client.list_agents()


async def create_agent_api(api_client, agent_data: Dict) -> Optional[Dict]:
    """Create agent via API."""
    return await api_client.create_agent(agent_data)


async def update_agent_api(api_client, agent_id: str, agent_data: Dict) -> Optional[Dict]:
    """Update agent via API."""
    return await api_client.update_agent(agent_id, agent_data)


async def delete_agent_api(api_client, agent_id: str) -> Optional[Dict]:
    """Delete agent via API."""
    return await api_client.delete_agent(agent_id)


def create_agent_form(tools_data: List[Dict]):
    """Create new agent form."""
    with st.form("create_agent_form", clear_on_submit=True):
        st.subheader("Create New Agent")
        
        agent_name = st.text_input("Agent Name *", placeholder="e.g., Research Assistant")
        agent_description = st.text_area("Agent Description", placeholder="Describe what this agent does...")
        
        col1, col2 = st.columns(2)
        with col1:
            model_type = st.selectbox("Model Type", ["gemini-pro", "gemini-pro-vision", "gemini-1.5-pro"])
        with col2:
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        
        system_prompt = st.text_area(
            "System Prompt *", 
            placeholder="You are a helpful AI assistant...",
            help="This defines the agent's behavior and personality"
        )
        
        # Tool Selection
        st.subheader("Select Tools")
        available_tool_names = [tool["name"] for tool in tools_data]
        selected_tools = st.multiselect(
            "Choose tools for this agent:",
            options=available_tool_names,
            help="Select multiple tools that this agent can use"
        )

        col1, col2 = st.columns(2)
        with col1:
            create_clicked = st.form_submit_button("Create Agent", type="primary")
        with col2:
            cancel_clicked = st.form_submit_button("Cancel")
        
        return {
            "create_clicked": create_clicked,
            "cancel_clicked": cancel_clicked,
            "agent_data": {
                "name": agent_name,
                "description": agent_description,
                "system_prompt": system_prompt,
                "model_name": model_type,
                "temperature": temperature,
                "tools": selected_tools
            } if agent_name and system_prompt else None
        }


def edit_agent_form(agent_to_edit: Dict, tools_data: List[Dict]):
    """Edit existing agent form."""
    with st.form("edit_agent_form", clear_on_submit=True):
        st.subheader(f"Edit Agent: {agent_to_edit['name']}")
        
        agent_name = st.text_input("Agent Name *", value=agent_to_edit['name'])
        agent_description = st.text_area("Agent Description", value=agent_to_edit.get('description', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            model_options = ["gemini-pro", "gemini-pro-vision", "gemini-1.5-pro"]
            current_model_index = 0
            if agent_to_edit.get('model_name') in model_options:
                current_model_index = model_options.index(agent_to_edit['model_name'])
            model_type = st.selectbox("Model Type", model_options, index=current_model_index)
        with col2:
            temperature = st.slider("Temperature", 0.0, 2.0, agent_to_edit.get('temperature', 0.7), 0.1)
        
        system_prompt = st.text_area(
            "System Prompt *", 
            value=agent_to_edit.get('system_prompt', ''),
            help="This defines the agent's behavior and personality"
        )
        
        # Tool Selection for editing
        st.subheader("Select Tools")
        available_tool_names = [tool["name"] for tool in tools_data]
        current_tools = agent_to_edit.get('tools', [])
        selected_tools = st.multiselect(
            "Choose tools for this agent:",
            options=available_tool_names,
            default=current_tools,
            help="Select multiple tools that this agent can use"
        )

        col1, col2 = st.columns(2)
        with col1:
            update_clicked = st.form_submit_button("Update Agent", type="primary")
        with col2:
            cancel_clicked = st.form_submit_button("Cancel")
        
        return {
            "update_clicked": update_clicked,
            "cancel_clicked": cancel_clicked,
            "agent_data": {
                "name": agent_name,
                "description": agent_description,
                "system_prompt": system_prompt,
                "model_name": model_type,
                "temperature": temperature,
                "tools": selected_tools
            } if agent_name and system_prompt else None
        }


def display_agents_table(agents_data: List[Dict]):
    """Display agents in a table format."""
    if not agents_data:
        st.info("No agents found. Create your first agent to get started!")
        return []
    
    actions = []
    for i, agent in enumerate(agents_data):
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 2, 1, 1, 1])
            
            with col1:
                st.write(f"**{agent['name']}**")
                if agent.get('description'):
                    description = agent['description']
                    display_desc = description[:50] + "..." if len(description) > 50 else description
                    st.caption(display_desc)
            
            with col2:
                st.write(f"🧠 {agent.get('model_name', 'N/A')}")
                st.caption(f"Temp: {agent.get('temperature', 'N/A')}")
            
            with col3:
                tools_display = ", ".join(agent.get('tools', [])) if agent.get('tools') else "No tools"
                st.write(f"🔧 {tools_display}")
            
            with col4:
                created_at = agent.get('created_at', 'N/A')
                display_date = created_at[:10] if created_at != 'N/A' else 'N/A'
                st.caption(f"Created: {display_date}")
            
            with col5:
                if st.button("✏️ Edit", key=f"edit_{agent['id']}"):
                    actions.append(("edit", str(agent['id'])))
            
            with col6:
                if st.button("🗑️ Delete", key=f"delete_{agent['id']}"):
                    actions.append(("delete", str(agent['id']), agent['name']))
            
            st.divider()
    
    return actions


def agent_management_section(api_client, tools_data: List[Dict]):
    """Main agent management section."""
    st.header("🤖 Agent Management")

    # Initialize session states
    if 'show_create_agent_modal' not in st.session_state:
        st.session_state.show_create_agent_modal = False
    if 'show_edit_agent_modal' not in st.session_state:
        st.session_state.show_edit_agent_modal = False
    if 'edit_agent_id' not in st.session_state:
        st.session_state.edit_agent_id = None
    if 'agents_data' not in st.session_state:
        st.session_state.agents_data = []

    # Load agents data
    with LoadingState("Loading agents..."):
        agents = safe_async_call(load_agents, api_client)
        if agents is not None:
            st.session_state.agents_data = agents

    # Create New Agent Button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Create New Agent", type="primary"):
            st.session_state.show_create_agent_modal = True

    # Create New Agent Modal
    if st.session_state.show_create_agent_modal:
        form_result = create_agent_form(tools_data)
        
        if form_result["create_clicked"]:
            if form_result["agent_data"]:
                with LoadingState("Creating agent..."):
                    result = safe_async_call(create_agent_api, api_client, form_result["agent_data"])
                    if result:
                        show_success_message(f"Agent '{form_result['agent_data']['name']}' created successfully!")
                        st.session_state.show_create_agent_modal = False
                        st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if form_result["cancel_clicked"]:
            st.session_state.show_create_agent_modal = False
            st.rerun()

    # Edit Agent Modal
    if st.session_state.show_edit_agent_modal and st.session_state.edit_agent_id:
        agent_to_edit = next(
            (agent for agent in st.session_state.agents_data if str(agent["id"]) == st.session_state.edit_agent_id), 
            None
        )
        
        if agent_to_edit:
            form_result = edit_agent_form(agent_to_edit, tools_data)
            
            if form_result["update_clicked"]:
                if form_result["agent_data"]:
                    with LoadingState("Updating agent..."):
                        result = safe_async_call(update_agent_api, api_client, st.session_state.edit_agent_id, form_result["agent_data"])
                        if result:
                            show_success_message(f"Agent '{form_result['agent_data']['name']}' updated successfully!")
                            st.session_state.show_edit_agent_modal = False
                            st.session_state.edit_agent_id = None
                            st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
            
            if form_result["cancel_clicked"]:
                st.session_state.show_edit_agent_modal = False
                st.session_state.edit_agent_id = None
                st.rerun()

    # Existing Agents Table
    st.subheader("Existing Agents")
    actions = display_agents_table(st.session_state.agents_data)
    
    # Handle actions
    for action in actions:
        if action[0] == "edit":
            st.session_state.show_edit_agent_modal = True
            st.session_state.edit_agent_id = action[1]
            st.rerun()
        elif action[0] == "delete":
            with LoadingState("Deleting agent..."):
                result = safe_async_call(delete_agent_api, api_client, action[1])
                if result:
                    show_success_message(f"Agent '{action[2]}' deleted successfully!")
                    st.rerun()