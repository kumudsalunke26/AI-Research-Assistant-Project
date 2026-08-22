import logging
import os


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.join(LOG_DIR, "rag_system.log"),
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)


# ============================================================
# LOGGER FUNCTION
# ============================================================

def get_logger(name: str):
    """
    Create and return a logger for the given module name.

    Parameters
    ----------
    name : str
        Name of the module requesting the logger.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    return logging.getLogger(name)