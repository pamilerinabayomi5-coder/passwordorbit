import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME", "passwordorbit.db")

if not BOT_TOKEN:
    raise ValueError("CRITICAL ERROR: BOT_TOKEN environment variable is not set.")

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("PasswordOrbitBot")
