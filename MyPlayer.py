import vlc
import time
from utils_logger import logger

class MyPlayer:
    def __init__(self, musicFileObj): 
        self.musicFileObj = musicFileObj
        self.musicFile = self.musicFileObj.fileObj
        self.player = vlc.MediaPlayer(self.musicFile)
    

    def stop(self):
        """Stop playing the file"""
        logger.info(f'Stopping file "{self.musicFile}"')
        self.player.stop()
        

    def play(self):
        """Play the file"""
        from datetime import datetime
        endTime = self.musicFileObj.fileTimeslot[1]
        endTime = datetime.strftime(endTime, "%I.%M %p")
        logger.info(f'Playing file "{self.musicFile}". End time is {endTime}')
        self.player.play()

        time.sleep(1)
        if not self.player.is_playing():
            logger.error(f'File {self.musicFile} is not playing.')
            return
        
        while True:
            if not self.player.is_playing():
                logger.info(f'File {self.musicFile} has stopped playing')
                break
            
            if self.musicFileObj.eligibileToPlayNow:
                time.sleep(1)
            else:
                logger.info(f"Stopping to play file {self.musicFile}")
                self.player.stop()
                break