import vlc
import time
from utils_logger import logger

# Instantiate Telegram bot
# from Telegrammer import Telegrammer
# tg = Telegrammer()

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
        msg = f'Playing file "{self.musicFile}". End time is {endTime}'
        logger.info(msg)
        # tg.sendMessage(msg)
        self.player.play()

        time.sleep(1)
        if not self.player.is_playing():
            logger.warning(f'File {self.musicFile} is not playing. Stopping player')
            self.player.stop()
            logger.info(f'Stopped player.')
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


    def setVolume(self, volumeLevel=100):
        """Set the volume level"""
        self.player.audio_set_volume(volumeLevel)


    def setVideoScale(videoScale=0.3):
        """Set video scale"""
        self.player.video_set_scale(videoScale)
