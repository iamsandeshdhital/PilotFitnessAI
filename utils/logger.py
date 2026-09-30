"""
Logging utility for Pilot Fitness Assessment AI Tool
"""

import logging
import os
from datetime import datetime
from functools import wraps


def setup_logger(name='pilot_fitness', log_file='pilot_fitness.log', level=logging.INFO):
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_action(action_type):
    """Decorator to log actions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = setup_logger()
            timestamp = datetime.utcnow().isoformat()
            logger.info(f"[{timestamp}] ACTION: {action_type} - Function: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"[{timestamp}] SUCCESS: {action_type}")
                return result
            except Exception as e:
                logger.error(f"[{timestamp}] ERROR: {action_type} - {str(e)}")
                raise
        return wrapper
    return decorator


class AuditLogger:
    """Audit logging for sensitive operations"""
    
    def __init__(self):
        self.logger = setup_logger('audit', 'audit.log')
    
    def log_assessment(self, pilot_id, assessor, result):
        """Log assessment execution"""
        self.logger.info(
            f"ASSESSMENT - Pilot: {pilot_id}, Assessor: {assessor}, "
            f"Score: {result.get('overall_score')}, Status: {result.get('fitness_status')}"
        )
    
    def log_data_access(self, user, pilot_id, data_type):
        """Log data access"""
        self.logger.info(
            f"DATA_ACCESS - User: {user}, Pilot: {pilot_id}, DataType: {data_type}"
        )
    
    def log_data_modification(self, user, pilot_id, data_type, action):
        """Log data modification"""
        self.logger.info(
            f"DATA_MODIFICATION - User: {user}, Pilot: {pilot_id}, "
            f"DataType: {data_type}, Action: {action}"
        )
    
    def log_security_event(self, event_type, details):
        """Log security events"""
        self.logger.warning(
            f"SECURITY_EVENT - Type: {event_type}, Details: {details}"
        )


# Global audit logger instance
audit_logger = AuditLogger()
