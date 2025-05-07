import seqlog
import logging
import sys
from pathlib import Path

def setup_logging() -> None:
    """
    Setup logging configuration for the entire project.

    """
    seqlog.configure_from_file(Path(__file__).parent / "log_config.yml")
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
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Prevent propagation to root logger
    root_logger.propagate = False

    logging.info(f"Logging setup completed")