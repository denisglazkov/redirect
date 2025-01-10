import logging

def setup_logger():
    """
    Configures the logger for the Flask application.
    """
    # Create a logger instance
    logger = logging.getLogger("flask-app")
    logger.setLevel(logging.INFO)

    # StreamHandler for local console logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    # New Relic will automatically instrument the logger when configured
    return logger