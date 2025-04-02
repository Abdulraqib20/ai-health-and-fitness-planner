import sys
import logging
from pathlib import Path
import tomli

project_root = Path(__file__).resolve().parent.parent
secrets_path = project_root / ".streamlit/secrets.toml"

# Initialize logger first to capture configuration errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'config/logs/config.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration variables that will be exported
CONFIG = {
    'GOOGLE_API_KEY': None,
    'GROQ_API_KEY': None,
}

try:
    # Load and validate configuration
    with open(secrets_path, "rb") as f:
        secrets = tomli.load(f)
    
    # Map configuration values
    CONFIG.update({
            'GOOGLE_API_KEY': secrets['GOOGLE']['API_KEY'],
            'GROQ_API_KEY': secrets['GROQ']['API_KEY'],
    })

    # Secure logging
    for key, value in CONFIG.items():
        hidden = f"{value[:2]}****{value[-2:]}" if value and len(value) > 4 else "****"
        logger.info(f"Loaded {key}: {hidden}")

except Exception as e:
    logger.critical(f"Configuration failed: {str(e)}")
    sys.exit(1)

# Export specific variables
GOOGLE_API_KEY = CONFIG['GOOGLE_API_KEY']
GROQ_API_KEY = CONFIG['GROQ_API_KEY']

__all__ = [
    'GOOGLE_API_KEY',
    'GROQ_API_KEY'
]