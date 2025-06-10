import streamlit as st

def agent_management_section():
    st.header("Agent Management")

    # Initialize session states
    if 'show_create_agent_modal' not in st.session_state:
        st.session_state.show_create_agent_modal = False
    if 'show_edit_agent_modal' not in st.session_state:
        st.session_state.show_edit_agent_modal = False
    if 'edit_agent_id' not in st.session_state:
        st.session_state.edit_agent_id = None

    # Available tools for selection
    available_tools = [
        {"id": "1", "name": "Web Search"},
        {"id": "2", "name": "File Reader"},
        {"id": "3", "name": "Calculator"},
        {"id": "4", "name": "Email Sender"},
        {"id": "5", "name": "Data Analyzer"}
    ]

    # Create New Agent Button
    if st.button("Create New Agent"):
        st.session_state.show_create_agent_modal = True

    # Create New Agent Modal
    if st.session_state.show_create_agent_modal:
        with st.form("create_agent_form", clear_on_submit=True):
            st.subheader("Create New Agent")
            
            agent_name = st.text_input("Agent Name")
            agent_description = st.text_area("Agent Description")
            model_type = st.selectbox("Model Type", ["Google Gemini", "OpenAI", "Anthropic"])
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
            
            # Tool Selection
            st.subheader("Select Tools")
            selected_tools = st.multiselect(
                "Choose tools for this agent:",
                options=[tool["name"] for tool in available_tools],
                help="Select multiple tools that this agent can use"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Create Agent"):
                    tools_text = ", ".join(selected_tools) if selected_tools else "No tools selected"
                    st.success(f"Agent '{agent_name}' created successfully with tools: {tools_text}")
                    st.session_state.show_create_agent_modal = False
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_create_agent_modal = False

    # Sample agents data with tools
    agents = [
        {"id": "1", "name": "Research Assistant", "model": "Gemini Pro", "description": "AI research helper", "tools": ["Web Search", "File Reader"]},
        {"id": "2", "name": "Coding Mentor", "model": "Gemini Advanced", "description": "Programming tutor", "tools": ["File Reader", "Calculator"]}
    ]

    # Edit Agent Modal
    if st.session_state.show_edit_agent_modal and st.session_state.edit_agent_id:
        # Find the agent to edit
        agent_to_edit = next((agent for agent in agents if agent["id"] == st.session_state.edit_agent_id), None)
        
        if agent_to_edit:
            with st.form("edit_agent_form", clear_on_submit=True):
                st.subheader(f"Edit Agent: {agent_to_edit['name']}")
                
                agent_name = st.text_input("Agent Name", value=agent_to_edit['name'])
                agent_description = st.text_area("Agent Description", value=agent_to_edit['description'])
                model_type = st.selectbox("Model Type", ["Google Gemini", "OpenAI", "Anthropic"], 
                                        index=0 if agent_to_edit['model'] == "Gemini Pro" else 1)
                temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
                
                # Tool Selection for editing
                st.subheader("Select Tools")
                selected_tools = st.multiselect(
                    "Choose tools for this agent:",
                    options=[tool["name"] for tool in available_tools],
                    default=agent_to_edit.get('tools', []),
                    help="Select multiple tools that this agent can use"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Agent"):
                        tools_text = ", ".join(selected_tools) if selected_tools else "No tools selected"
                        st.success(f"Agent '{agent_name}' updated successfully with tools: {tools_text}")
                        st.session_state.show_edit_agent_modal = False
                        st.session_state.edit_agent_id = None
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.show_edit_agent_modal = False
                        st.session_state.edit_agent_id = None

    # Existing Agents Table
    st.subheader("Existing Agents")
    
    # Create interactive table with buttons
    for i, agent in enumerate(agents):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 1, 1])
            
            with col1:
                st.write(f"**{agent['name']}**")
            with col2:
                st.write(agent['model'])
            with col3:
                tools_display = ", ".join(agent.get('tools', [])) if agent.get('tools') else "No tools"
                st.write(f"Tools: {tools_display}")
            with col4:
                if st.button("Edit", key=f"edit_{agent['id']}"):
                    st.session_state.show_edit_agent_modal = True
                    st.session_state.edit_agent_id = agent['id']
                    st.rerun()
            with col5:
                if st.button("Delete", key=f"delete_{agent['id']}"):
                    st.warning(f"Delete functionality for {agent['name']} - To be implemented")
            
            st.divider()

def chat_interface():
    st.header("Agent Chat")

    selected_agent = st.selectbox("Choose an Agent",
        ["Research Assistant", "Coding Mentor", "General Assistant"])

    st.subheader("Chat History")
    chat_history = [
        {"role": "user", "message": "Hello, can you help me?"},
        {"role": "assistant", "message": "Sure! What can I assist you with today?"}
    ]

    for message in chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['message'])
        else:
            st.chat_message("assistant").write(message['message'])

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write("Processing your request...")

def tool_management_section():
    st.header("Tool Management")

    # Create New Tool Modal
    if 'show_create_tool_modal' not in st.session_state:
        st.session_state.show_create_tool_modal = False

    # Create New Tool Button
    if st.button("Create New Tool"):
        st.session_state.show_create_tool_modal = True

    # Create New Tool Modal
    if st.session_state.show_create_tool_modal:
        with st.form("create_tool_form", clear_on_submit=True):
            st.subheader("Create New Tool")
            
            tool_name = st.text_input("Tool Name")
            tool_description = st.text_area("Tool Description")
            tool_type = st.selectbox("Tool Type", ["API Integration", "Data Processing", "File Handler", "Web Scraper", "Calculator"])
            tool_category = st.selectbox("Category", ["Utility", "Data", "Communication", "Analysis", "Custom"])

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Create Tool"):
                    st.success(f"Tool {tool_name} created successfully!")
                    st.session_state.show_create_tool_modal = False
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_create_tool_modal = False

    # Existing Tools Table
    st.subheader("Existing Tools")
    
    # Sample tools data
    tools = [
        {"id": "1", "name": "Web Search", "type": "API Integration", "description": "Search the web for information"},
        {"id": "2", "name": "File Reader", "type": "File Handler", "description": "Read and process various file formats"},
        {"id": "3", "name": "Calculator", "type": "Calculator", "description": "Perform mathematical calculations"}
    ]

    # Create table with edit and delete options
    table_data = []
    for tool in tools:
        table_data.append({
            "Name": tool['name'], 
            "Type": tool['type'], 
            "Description": tool['description'],
            "Actions": f"[Edit] [Delete]"
        })

    # Display the table
    st.table(table_data)

def system_monitoring():
    st.header("System Health")

    st.metric("API Status", "🟢 Operational")
    st.metric("LLM Connection", "🟢 Connected to Google Gemini")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("CPU Usage", "25%")
    with col2:
        st.metric("Memory Usage", "1.2 GB / 8 GB")

    st.subheader("Recent API Calls")
    recent_calls = [
        {"endpoint": "/api/v1/chat/message", "status": "Success", "timestamp": "2 mins ago"},
        {"endpoint": "/api/v1/agent/create", "status": "Success", "timestamp": "5 mins ago"}
    ]

    for call in recent_calls:
        st.write(f"{call['endpoint']} - {call['status']} ({call['timestamp']})")

def main():
    st.title("FastAPI Agent Backend UI")

    page = st.sidebar.selectbox("Navigate", [
        "Home",
        "Agent Management",        "Tool Management",        "Chat Interface",
        "System Monitoring"
    ])

    if page == "Home":
        st.header("Welcome to Agent Backend")
        st.write("Use the sidebar to navigate different sections")

    elif page == "Agent Management":
        agent_management_section()
    elif page == "Tool Management":
        tool_management_section()
    elif page == "Chat Interface":
        chat_interface()

    elif page == "System Monitoring":
        system_monitoring()

if __name__ == "__main__":
    main()