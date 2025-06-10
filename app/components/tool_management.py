"""Tool management UI component."""

import streamlit as st
from typing import Dict, List, Optional

from app.utils.error_handler import safe_async_call, LoadingState, show_success_message


async def load_tools(api_client) -> Optional[List[Dict]]:
    """Load tools from API."""
    return await api_client.list_tools()


async def create_tool_api(api_client, tool_data: Dict) -> Optional[Dict]:
    """Create tool via API."""
    return await api_client.create_tool(tool_data)


async def delete_tool_api(api_client, tool_id: str) -> Optional[Dict]:
    """Delete tool via API."""
    return await api_client.delete_tool(tool_id)


def create_tool_form():
    """Create new tool form."""
    with st.form("create_tool_form", clear_on_submit=True):
        st.subheader("Create New Tool")
        
        tool_name = st.text_input("Tool Name *", placeholder="e.g., Web Search")
        tool_description = st.text_area("Tool Description", placeholder="Describe what this tool does...")
        
        col1, col2 = st.columns(2)
        with col1:
            tool_type = st.selectbox("Tool Type", [
                "API Integration", 
                "Data Processing", 
                "File Handler", 
                "Web Scraper", 
                "Calculator",
                "Communication",
                "Analysis"
            ])
        with col2:
            tool_category = st.selectbox("Category", [
                "Utility", 
                "Data", 
                "Communication", 
                "Analysis", 
                "Custom"
            ])

        col1, col2 = st.columns(2)
        with col1:
            create_clicked = st.form_submit_button("Create Tool", type="primary")
        with col2:
            cancel_clicked = st.form_submit_button("Cancel")
        
        return {
            "create_clicked": create_clicked,
            "cancel_clicked": cancel_clicked,
            "tool_data": {
                "name": tool_name,
                "description": tool_description,
                "tool_type": tool_type,
                "category": tool_category
            } if tool_name else None
        }


def display_tools_table(tools_data: List[Dict]):
    """Display tools in a table format."""
    if not tools_data:
        st.info("No tools found. Create your first tool to get started!")
        return []
    
    actions = []
    for i, tool in enumerate(tools_data):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1.5, 2, 1, 1])
            
            with col1:
                st.write(f"**{tool['name']}**")
                if tool.get('description'):
                    description = tool['description']
                    display_desc = description[:50] + "..." if len(description) > 50 else description
                    st.caption(display_desc)
            
            with col2:
                st.write(f"🏷️ {tool.get('tool_type', 'N/A')}")
            
            with col3:
                st.write(f"📂 {tool.get('category', 'N/A')}")
            
            with col4:
                status = "✅ Active" if tool.get('is_enabled', True) else "❌ Disabled"
                st.write(status)
            
            with col5:
                if st.button("🗑️ Delete", key=f"delete_tool_{tool['id']}"):
                    actions.append(("delete", str(tool['id']), tool['name']))
            
            st.divider()
    
    return actions


def tool_management_section(api_client):
    """Main tool management section."""
    st.header("🔧 Tool Management")

    # Initialize session states
    if 'show_create_tool_modal' not in st.session_state:
        st.session_state.show_create_tool_modal = False
    if 'tools_data' not in st.session_state:
        st.session_state.tools_data = []

    # Load tools data
    with LoadingState("Loading tools..."):
        tools = safe_async_call(load_tools, api_client)
        if tools is not None:
            st.session_state.tools_data = tools

    # Create New Tool Button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Create New Tool", type="primary"):
            st.session_state.show_create_tool_modal = True

    # Create New Tool Modal
    if st.session_state.show_create_tool_modal:
        form_result = create_tool_form()
        
        if form_result["create_clicked"]:
            if form_result["tool_data"]:
                with LoadingState("Creating tool..."):
                    result = safe_async_call(create_tool_api, api_client, form_result["tool_data"])
                    if result:
                        show_success_message(f"Tool '{form_result['tool_data']['name']}' created successfully!")
                        st.session_state.show_create_tool_modal = False
                        st.rerun()
            else:
                st.error("Please fill in the tool name")
        
        if form_result["cancel_clicked"]:
            st.session_state.show_create_tool_modal = False
            st.rerun()

    # Existing Tools Table
    st.subheader("Existing Tools")
    actions = display_tools_table(st.session_state.tools_data)
    
    # Handle actions
    for action in actions:
        if action[0] == "delete":
            with LoadingState("Deleting tool..."):
                result = safe_async_call(delete_tool_api, api_client, action[1])
                if result:
                    show_success_message(f"Tool '{action[2]}' deleted successfully!")
                    st.rerun()