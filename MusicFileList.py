from pathlib import Path
from MusicFile import MusicFile
import random

extensionMusicFiles = [".mp3", ".wav", ".ogg", ".flac", ".m4a", ".wma", ".aac", ".aiff", ".ape", ".au", ".mka", ".opus", ".ra", ".rm", ".tta", ".wv", ".m4b", ".m4p", ".mpc"]
optionalExtensions = [".mp4", ".mpeg"]
extensionMusicFiles.extend(optionalExtensions)
extensionMusicFiles = [i.lower() for i in extensionMusicFiles]


class MusicFileList:
    def __init__(self, folderPath, randomize=False) -> None:
        self.rootFolder = Path(folderPath)
        
        self.fileList = []
        self.randomize = randomize

        # Get all files from the folder
        for file_path in Path(folderPath).rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensionMusicFiles:
                self.fileList.append(file_path)

        # Randomize the list
        if self.randomize:
            random.shuffle(self.fileList)


    def __str__(self) -> str:
        return f'MusicFileList({len(self.fileList)} files from path "{self.rootFolder}")'
    

    def __iter__(self):
        """Return iterator object"""
        for f in self.fileList:
            yield MusicFile(self.rootFolder, f)
    
    def __len__(self):
        """Return number of files in the list"""
        return len(self.fileList)

    @property
    def eligibleToPlayNow(self):
        """Return list of files eligible to play now"""

        # if self.randomize:
        #     random.shuffle(self.fileList)

        for f in self.fileList:
            mf = MusicFile(self.rootFolder, f)
            if mf.eligibileToPlayNow:
                yield mf

    @property
    def eligibleToPlayNowCount(self):
        """Return number of files eligible to play now"""
        
        count = 0
        for _ in self.eligibleToPlayNow:
            count += 1
        return count

if __name__ == "__main__":
    folderPath = r"d:\library music"
    mList = MusicFileList(folderPath)
    print(mList)
