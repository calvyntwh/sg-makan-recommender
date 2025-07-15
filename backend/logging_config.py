"""Logging configuration for the Singapore Makan Recommender."""

import logging
import sys
from typing import Optional

from .config import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """Set up logging configuration for the application.
    
    Args:
        log_level: Override the default log level from settings
        
    Returns:
        Configured logger instance
    """
    level = log_level or settings.log_level
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create application-specific logger
    logger = logging.getLogger('sg_makan_recommender')
    
    # Suppress noisy third-party loggers in production
    if level.upper() not in ['DEBUG']:
        logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    
    return logger


# Global logger instance
logger = setup_logging()
