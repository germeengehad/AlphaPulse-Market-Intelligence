import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists and return the Path object.
    Accepts str or Path.
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def validate_env_variables(vars_dict: dict):
    """
    Validate that all required environment variables are provided.

    Raises:
        ValueError: If any required variables are missing.
    """
    missing = [key for key, value in vars_dict.items() if not value]

    if missing:
        message = f"❌ Missing environment variables: {', '.join(missing)}"
        logger.error(message)
        raise ValueError(message)

    logger.info("✅ All required environment variables are set.")
