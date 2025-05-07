import seqlog
import logging
from pathlib import Path

def setup_logging() -> None:
    """
    Setup logging configuration for the entire project.

    """
    seqlog.configure_from_file(Path(__file__).parent / "log_config.yml")

    logger = logging.getLogger(__name__)

    logger.info(f"Logging setup completed")