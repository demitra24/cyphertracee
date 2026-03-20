import logging

# --- LOGGING CONFIGURATION ---
LOG_FORMAT = '%(asctime)s - %(levelname)s - [%(event_type)s] from %(source_ip)s - %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("backend_security.log"),
        logging.StreamHandler()
    ]
)

# Get a logger instance that other modules can import
logger = logging.getLogger(__name__)