import logging
import colorlog


def setup_logger(name=__name__):
    """
    Set up a logger with color support that can be imported and used in other modules.

    :param name: Name of the logger (usually the module name)
    :return: Configured logger instance
    """
    # Create a logger
    logger = logging.getLogger(name)

    # If the logger already has handlers, return it to prevent adding multiple handlers
    if logger.hasHandlers():
        return logger

    # Set the minimum logging level
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Define a colored formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(module)s.%(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    file_handler = logging.FileHandler(f"errorlog")
    file_handler.setLevel(logging.ERROR)  # Only log errors and critical messages to the file
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger