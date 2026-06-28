from loguru import logger
import os

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Remove default logger
logger.remove()

# Log to file
logger.add(
    "logs/orunodoi.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# Log to terminal
logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
)