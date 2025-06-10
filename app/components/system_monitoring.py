"""System monitoring UI component."""

import streamlit as st
from typing import Dict, List

from app.utils.error_handler import safe_async_call, LoadingState


def display_system_metrics(agents_count: int, tools_count: int):
    """Display system metrics."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("API Status", "🟢 Online", "Healthy")
    
    with col2:
        st.metric("Total Agents", agents_count)
    
    with col3:
        st.metric("Total Tools", tools_count)


def api_health_check_section(api_client):
    """API health check section."""
    st.subheader("API Health Check")
    if st.button("Check API Health"):
        with LoadingState("Checking API health..."):
            try:
                health_result = safe_async_call(api_client.health_check)
                if health_result:
                    st.success("✅ API is healthy and responding")
                    st.json(health_result)
            except Exception as e:
                st.error(f"❌ API health check failed: {str(e)}")


def system_monitoring(api_client, agents_data: List[Dict], tools_data: List[Dict]):
    """Main system monitoring section."""
    st.header("📊 System Monitoring")

    # Display metrics
    agents_count = len(agents_data)
    tools_count = len(tools_data)
    display_system_metrics(agents_count, tools_count)

    # API Health Check
    api_health_check_section(api_client)

    # Recent Activity (placeholder)
    st.subheader("Recent Activity")
    st.info("Recent activity tracking will be implemented in future updates.")