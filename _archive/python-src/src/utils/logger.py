"""
Structured Logging Utility for VibeGraph Backend

This module provides structured JSON logging for all backend services.
Logs are formatted as JSON for easy parsing and aggregation.
"""

import json
import logging
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    
    Formats log records as JSON objects with consistent structure:
    - timestamp: ISO 8601 timestamp
    - level: Log level (INFO, ERROR, etc.)
    - logger: Logger name
    - message: Log message
    - context: Additional context data
    - error: Error details (for exceptions)
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON string representation of log record
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Add context data if present
        if hasattr(record, 'context'):
            log_data['context'] = record.context
        
        # Add error details for exceptions
        if record.exc_info:
            log_data['error'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else None,
                'message': str(record.exc_info[1]) if record.exc_info[1] else None,
                'traceback': self.formatException(record.exc_info) if record.exc_info else None
            }
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'message', 'pathname', 'process', 'processName',
                          'relativeCreated', 'thread', 'threadName', 'exc_info',
                          'exc_text', 'stack_info', 'context']:
                log_data[key] = value
        
        return json.dumps(log_data)


def setup_structured_logging(
    log_level: str = 'INFO',
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up structured JSON logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        
    Returns:
        Configured root logger
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Create JSON formatter
    json_formatter = JSONFormatter()
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LogContext:
    """
    Context manager for adding structured context to log messages.
    
    Usage:
        with LogContext(logger, request_id='123', user_id='456'):
            logger.info('Processing request')
    """
    
    def __init__(self, logger: logging.Logger, **context):
        """
        Initialize log context.
        
        Args:
            logger: Logger instance
            **context: Context key-value pairs
        """
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        """Enter context manager."""
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.context = self.context
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


def log_api_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration: float,
    **context
):
    """
    Log API request with structured data.
    
    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration: Request duration in seconds
        **context: Additional context data
    """
    log_data = {
        'method': method,
        'path': path,
        'status_code': status_code,
        'duration_ms': round(duration * 1000, 2),
        **context
    }
    
    with LogContext(logger, **log_data):
        logger.info(f'{method} {path} - {status_code} ({duration:.3f}s)')


def log_handler_execution(
    logger: logging.Logger,
    handler_name: str,
    duration: float,
    success: bool = True,
    **context
):
    """
    Log handler execution time with structured data.
    
    Args:
        logger: Logger instance
        handler_name: Name of the handler
        duration: Execution duration in seconds
        success: Whether execution was successful
        **context: Additional context data
    """
    log_data = {
        'handler': handler_name,
        'duration_ms': round(duration * 1000, 2),
        'success': success,
        **context
    }
    
    with LogContext(logger, **log_data):
        status = 'completed' if success else 'failed'
        logger.info(f'Handler {handler_name} {status} in {duration:.3f}s')


def filter_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter sensitive data from log context.
    
    Removes or masks:
    - JWT tokens
    - Raw quiz answers
    - Embedding vectors
    - Passwords
    - API keys
    
    Args:
        data: Data dictionary to filter
        
    Returns:
        Filtered data dictionary
    """
    sensitive_keys = {
        'token', 'authorization', 'password', 'secret', 'api_key',
        'jwt', 'bearer', 'answers', 'vector', 'embedding'
    }
    
    filtered = {}
    for key, value in data.items():
        key_lower = key.lower()
        
        # Check if key contains sensitive data
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            filtered[key] = '[REDACTED]'
        elif isinstance(value, dict):
            filtered[key] = filter_sensitive_data(value)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            filtered[key] = [filter_sensitive_data(item) for item in value]
        else:
            filtered[key] = value
    
    return filtered
