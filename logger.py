import logging
import os
from datetime import datetime

# This will just create the file name
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"

# This is the directory where logs will be stored
logs_path = os.path.join(os.getcwd(), "logs")

# Create the directory if it doesn't exist
os.makedirs(logs_path, exist_ok=True)

# Now create full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Setting up logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# expose logger object
logger = logging.getLogger(__name__)