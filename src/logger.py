"""
This module provides logging functionality for the PillTracker application.

It sets up a logger that writes log messages to a file with the current date as the filename.
The log file is stored in the 'logs' directory relative to the current working directory.

Example usage:
    import logger

    logger.logging.info("Logging started")
    logger.logging.info("Logging completed")
"""

import os
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == "__main__":
    logging.info("Logging started")
    logging.info("Logging completed")
