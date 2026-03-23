# config/base_config.py
import os
import logging
from utils.base_utils import ensure_dir
from dotenv import load_dotenv
from utils.base_utils import validate_env_variables

# ============================================================
# 📁 Base Directories
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "processed_data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Ensure directories exist
for directory in [
    LOG_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    NOTEBOOKS_DIR,
    TEMP_DIR,
    REPORTS_DIR,
]:
    ensure_dir(directory)

# ============================================================
# 🟥 Logging Configuration
# ============================================================
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("YahooFinanceApp")

# ============================================================
# 🔵 Load Environment Variables
# ============================================================
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Validate important env vars
validate_env_variables(
    {
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
        "DB_HOST": DB_HOST,
        "DB_PORT": DB_PORT,
        "DB_NAME": DB_NAME,
    }
)
