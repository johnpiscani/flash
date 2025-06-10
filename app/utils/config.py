"""Configuration management for Streamlit app."""

import os
from typing import Optional
import streamlit as st


class StreamlitConfig:
    """Configuration for Streamlit application."""
    
    def __init__(self):
        """Initialize configuration."""
        self.api_base_url = self._get_config_value("API_BASE_URL", "http://localhost:8000")
        self.api_key = self._get_config_value("API_KEY", None)
        self.debug = self._get_config_value("DEBUG", "false").lower() == "true"
        self.page_title = self._get_config_value("PAGE_TITLE", "AI Agent Management")
        self.page_icon = self._get_config_value("PAGE_ICON", "🤖")
    
    def _get_config_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value from various sources."""
        # Priority: Streamlit secrets > Environment variables > Default
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except:
            pass
        
        # Try environment variables
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value
        
        # Return default
        return default


# Singleton instance
@st.cache_resource
def get_config() -> StreamlitConfig:
    """Get cached configuration instance."""
    return StreamlitConfig()