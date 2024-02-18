from MusicFileList import MusicFileList
from MusicFile import MusicFile
from utils_logger import logger
from MyPlayer import MyPlayer
import os, time
from pathlib import Path
import portalocker

# Open the file again - as a lock to prevent multiple instances
logger.info(f"{os.getpid()} - Locking Singleton...")
lock1 = portalocker.Lock('singleton')
try:
    if lock1.acquire():
        logger.info(f"{os.getpid()} - Singleton lock acquired.")
except portalocker.exceptions.LockException:
    logger.error(f"{os.getpid()} - Singleton lock failed. Another instance is already running.")
    import sys; sys.exit()

# Start logging of new instance/session
logger.info(f'{os.getpid()} - {"*"*10} New instance/session started {"*"*10}')

libraryPath = r"f:\library music"
waitTimeForNewFile = 30
sleepyFromTime = "2215"
sleepyToTime = "0600"
sleepyVolume = 30


def parse_time(time_str):
    """Convert a string in format "HHMM" to a time object"""
    from datetime import time
    return time(int(time_str[:2]), int(time_str[2:]))


def is_time_between(begin_time_str, end_time_str):
    """Checks if current time is between two given time points. Returns bool."""

    from datetime import datetime
    begin_time = parse_time(begin_time_str)
    end_time = parse_time(end_time_str)
    current_time = datetime.now().time()

    if begin_time < end_time:
        return begin_time <= current_time <= end_time
    else:
        # Handles cases where the range crosses midnight (e.g., 10 PM to 4 AM)
        return begin_time <= current_time or current_time < end_time


while True:
    
##    # While the current time is before 6 AM, wait for 1 min
##    while time.localtime().tm_hour < 6:
##        logger.info(f"Current time is before 6 AM. {time.strftime('%I:%M %p')}. Waiting for 1 minute")
##        time.sleep(60)
##    
##    # If current time is after 10:15 PM, wait for 1 min
##    import datetime
##    while True:
##        today = datetime.datetime.today()
##        if datetime.datetime.now() < datetime.datetime.combine(today, datetime.time(22, 15)):
##            break
##        else:
##            logger.info(f"Current time is after 10:15 PM. {time.strftime('%I:%M %p')}. Waiting for 1 minute")
##            time.sleep(60)

    # Initialize MusicFileList
    mList = MusicFileList(libraryPath, randomize=False)
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
        
        if is_time_between(sleepyFromTime, sleepyToTime):
            logger.info(f"Volume reduced to {sleepyVolume}%")
            mp.setVolume(sleepyVolume)
        else:
            logger.info(f"Volume reset to 100%")
            mp.setVolume(100)

            
        logger.info(f"Playing file {musicFile.fileObj}")
        playingStatus = mp.play()
