import logging

logger = logging.getLogger("nids logger")
logger.setLevel(logging.INFO)

# Create handlers (e.g., console and file handlers)
file_handler = logging.FileHandler("app.log")

# Set log levels for the handlers
file_handler.setLevel(logging.INFO)  # Only warnings and above go to file

# Create and set formatters for the handlers
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
