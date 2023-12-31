from MusicFileList import MusicFileList
from MusicFile import MusicFile
from utils_logger import logger
from MyPlayer import MyPlayer
import time

# Create a temp file if not exists
with open("singleton", "a") as f:
    # Enter the current datetime in the file
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Open the file again - as a lock to prevent multiple instances
try:
    open("singleton", "w") 
except IOError:
    logger.error("Another instance is already running. Exiting...")
    exit(0)

# Start logging of new instance/session
logger.info(f'{"*"*10} New instance/session started {"*"*10}')

libraryPath = r"d:\library music"
waitTimeForNewFile = 30

while True:
    
    # While the current time is before 6 AM, wait for 1 min
    while time.localtime().tm_hour < 6:
        logger.info(f"Current time is before 6 AM. {time.strftime('%I:%M %p')}. Waiting for 1 minute")
        time.sleep(60)
    
    # If current time is after 10:15 PM, wait for 1 min
    import datetime
    while True:
        today = datetime.datetime.today()
        if datetime.datetime.now() < datetime.datetime.combine(today, datetime.time(22, 15)):
            break
        else:
            logger.info(f"Current time is after 10:15 PM. {time.strftime('%I:%M %p')}. Waiting for 1 minute")
            time.sleep(60)

    # Initialize MusicFileList
    mList = MusicFileList(libraryPath, randomize=True)
    logger.info(mList)

    # Get files eligible to play now
    filesToPlay = None
    filesToPlay = mList.eligibleToPlayNow

    # No file to play now and no default folder to play
    if mList.eligibleToPlayNowCount == 0:
        logger.info(f"No files to play now. Waiting for {waitTimeForNewFile} seconds")
        time.sleep(waitTimeForNewFile)
        continue
    else:
        logger.info(f"{mList.eligibleToPlayNowCount} files are eligible to play now")

    for musicFile in filesToPlay:
        mp = MyPlayer(musicFile)
        
        # if musicFile.fileTimeslot[1].hour < 23:
        logger.info(f"Playing file {musicFile.fileObj}")
        playingStatus = mp.play()