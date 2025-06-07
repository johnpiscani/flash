"""Logging utilities."""

import logging
import sys
from typing import Optional

from app.core.config import settings


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Set up logger with consistent formatting."""
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        # Create handler
        handler = logging.StreamHandler(sys.stdout)
        
        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Set level
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    return logger


# Create default logger
logger = setup_logger("fastapi_agent")