from MusicFileList import MusicFileList
from MusicFile import MusicFile
from utils_logger import logger
from MyPlayer import MyPlayer
import time

# Start logging of new instance/session
logger.info(f'{"*"*10} New instance/session started {"*"*10}')

libraryPath = r"d:\library music"
waitTimeForNewFile = 30

while True:
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

    for musicFile in filesToPlay:
        mp = MyPlayer(musicFile)
        if musicFile.fileTimeslot[1].hour < 22:
            playingStatus = mp.play()