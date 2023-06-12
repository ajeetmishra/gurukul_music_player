import logging
import os
from datetime import datetime as dt


# Initiate logger
log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

# Check if folder data/logs exists
if not os.path.exists('logs'):
    # Create folder data/logs
    os.makedirs('logs')
    
fnameLog = os.path.join('logs', f'{dt.now().strftime("%Y-%m-%d")}.log')

# Define basic configuration
logging.basicConfig(
    # Define logging level
    level=logging.INFO,
    # Define the format of log messages
    format=log_format,
    # Provide the filename to store the log messages
    filename=fnameLog,
    # Provide the date format
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define your own logger name
logger = logging.getLogger('init')