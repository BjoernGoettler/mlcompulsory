import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logging(
    log_file: Optional[str] = None,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_file_size: int = 1024 * 1024,  # 1MB
    backup_count: int = 5
) -> None:
    """
    Setup logging configuration for the entire project.
    
    Args:
        log_file: Path to log file. If None, logs will only go to console
        console_level: Logging level for console output
        file_level: Logging level for file output
        max_file_size: Maximum size of log file before rotation (in bytes)
        backup_count: Number of backup files to keep
    """
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set to lowest level, handlers will filter

    # Remove existing handlers to avoid duplicates
    root_logger.handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if log_file is specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Prevent propagation to root logger
    root_logger.propagate = False

    logging.info(f"Logging setup completed. Console level: {console_level}, File level: {file_level}")