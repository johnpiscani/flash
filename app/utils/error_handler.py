"""Error handling utilities for Streamlit app."""

import streamlit as st
from typing import Callable, Any
import asyncio
import functools


def handle_api_errors(func: Callable) -> Callable:
    """Decorator to handle API errors gracefully for async functions."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            
            # Parse different types of errors
            if "Connection Error" in error_message:
                st.error("🔌 **Connection Error**: Unable to connect to the API server. Please check if the backend is running.")
            elif "API Error (401)" in error_message:
                st.error("🔐 **Authentication Error**: Invalid or missing API credentials.")
            elif "API Error (404)" in error_message:
                st.error("🔍 **Not Found**: The requested resource was not found.")
            elif "API Error (400)" in error_message:
                st.error(f"⚠️ **Validation Error**: {error_message}")
            elif "API Error (500)" in error_message:
                st.error("🚨 **Server Error**: Internal server error occurred. Please try again later.")
            else:
                st.error(f"❌ **Error**: {error_message}")
            
            return None
    
    return wrapper


def handle_sync_api_errors(func: Callable) -> Callable:
    """Decorator to handle API errors for functions that call async functions."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            
            # Parse different types of errors
            if "Connection Error" in error_message:
                st.error("🔌 **Connection Error**: Unable to connect to the API server. Please check if the backend is running.")
            elif "API Error (401)" in error_message:
                st.error("🔐 **Authentication Error**: Invalid or missing API credentials.")
            elif "API Error (404)" in error_message:
                st.error("🔍 **Not Found**: The requested resource was not found.")
            elif "API Error (400)" in error_message:
                st.error(f"⚠️ **Validation Error**: {error_message}")
            elif "API Error (500)" in error_message:
                st.error("🚨 **Server Error**: Internal server error occurred. Please try again later.")
            else:
                st.error(f"❌ **Error**: {error_message}")
            
            return None
    
    return wrapper


def safe_async_call(async_func, *args, **kwargs):
    """Safely call an async function and handle errors."""
    try:
        return asyncio.run(async_func(*args, **kwargs))
    except Exception as e:
        error_message = str(e)
        
        # Parse different types of errors
        if "Connection Error" in error_message:
            st.error("🔌 **Connection Error**: Unable to connect to the API server. Please check if the backend is running.")
        elif "API Error (401)" in error_message:
            st.error("🔐 **Authentication Error**: Invalid or missing API credentials.")
        elif "API Error (404)" in error_message:
            st.error("🔍 **Not Found**: The requested resource was not found.")
        elif "API Error (400)" in error_message:
            st.error(f"⚠️ **Validation Error**: {error_message}")
        elif "API Error (500)" in error_message:
            st.error("🚨 **Server Error**: Internal server error occurred. Please try again later.")
        else:
            st.error(f"❌ **Error**: {error_message}")
        
        return None


def show_loading_spinner(message: str = "Loading..."):
    """Show loading spinner with message."""
    return st.spinner(message)


def show_success_message(message: str):
    """Show success message."""
    st.success(f"✅ {message}")


def show_info_message(message: str):
    """Show info message."""
    st.info(f"ℹ️ {message}")


def show_warning_message(message: str):
    """Show warning message."""
    st.warning(f"⚠️ {message}")


class LoadingState:
    """Context manager for loading states."""
    
    def __init__(self, message: str = "Loading..."):
        self.message = message
        self.spinner = None
    
    def __enter__(self):
        self.spinner = st.spinner(self.message)
        self.spinner.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.spinner:
            self.spinner.__exit__(exc_type, exc_val, exc_tb)