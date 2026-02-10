import logging
import sys
import os
from src.config import settings

# Ensure logs directory exists
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def setup_logging():
    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(settings.LOG_LEVEL)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Avoid duplicate logs if handler already exists
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

logger = setup_logging()

def get_search_logger(search_id: str):
    """
    Creates or retrieves a logger for a specific search_id.
    Logs are saved to logs/{search_id}/app.log
    """
    search_log_dir = os.path.join(LOGS_DIR, search_id)
    if not os.path.exists(search_log_dir):
        os.makedirs(search_log_dir)

    log_file = os.path.join(search_log_dir, "app.log")
    
    # Use a unique name for this logger to avoid conflict with the main logger
    logger_name = f"{settings.APP_NAME}.{search_id}"
    search_logger = logging.getLogger(logger_name)
    search_logger.setLevel(settings.LOG_LEVEL)

    # Check if handler already exists to avoid duplication
    if not any(isinstance(h, logging.FileHandler) for h in search_logger.handlers):
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        search_logger.addHandler(file_handler)
    
    # Also propagate to root logger if desired, or add console handler?
    # Defaults propagate=True, so it will go up to APP_NAME logger and print to console.
    
    return search_logger
