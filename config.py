import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
logger.info("Environment variables loaded")

class Config:
    """Configuration settings for FinSight"""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    # Using a more recent and capable model is recommended
    OPENAI_MODEL = "gpt-4o"

    # File Paths
    BASE_DIR = Path(__file__).parent
    OUTPUT_DIR = BASE_DIR / "output"
    EXTRACTIONS_DIR = BASE_DIR / "extractions"

    # Agent Configuration
    AGENT_VERBOSE = True
    MAX_PASSWORD_ATTEMPTS = 3

    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        logger.info("Setting up project directories")
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.EXTRACTIONS_DIR.mkdir(exist_ok=True)
        logger.info(f"Directories ensured: {cls.OUTPUT_DIR}, {cls.EXTRACTIONS_DIR}")

# Initialize directories
logger.info("Initializing configuration")
Config.setup_directories()
logger.info("Configuration initialized successfully")