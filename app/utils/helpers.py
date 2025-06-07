"""Helper functions."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import UUID


def generate_api_key() -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(32)


def hash_string(text: str) -> str:
    """Hash a string using SHA-256."""
    return hashlib.sha256(text.encode()).hexdigest()


def is_valid_uuid(uuid_string: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


def format_response(
    success: bool = True,
    message: str = "Operation completed successfully",
    data: Optional[Any] = None,
    errors: Optional[Dict] = None
) -> Dict:
    """Format a standard API response."""
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    if errors:
        response["errors"] = errors
    
    return response


def calculate_token_estimate(text: str) -> int:
    """Rough estimate of token count for text."""
    # Very rough estimate: ~4 characters per token
    return len(text) // 4


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."