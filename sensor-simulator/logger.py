import logging
import os
from datetime import datetime
import sys

# LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE = f"{os.environ.get('SENSOR-ID', 1)}.log"
# logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
logs_path=os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    format = "%(asctime)s [%(levelname)-8s] %(lineno)-5d %(name)-10s - %(message)s",
    level = logging.INFO,

    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE_PATH)
    ]
)