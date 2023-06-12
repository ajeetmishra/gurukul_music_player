import pathlib, re, datetime
from utils_logger import logger

class InvalidTimePoint(Exception):
    """Time is not in XX.XX AM or XX.XX pm format"""
    pass

class MusicFile:
    def __init__(self, rootFolder, filePath) -> None:
        self.rootFolder = pathlib.Path(rootFolder)
        self.fileObj    = pathlib.Path(filePath)
        # self.fileExtn   = self.fileObj.suffix.lower()

    
    @property
    def eligibileToPlayNow(self):
        """Check if the file is eligible to play now"""

        # Get current day of week
        currentWeekDay = datetime.datetime.today().strftime("%A")
        
        # Get current time. Convert to datetime object
        now = datetime.datetime.now().strftime("%H:%M:%S")
        now = datetime.datetime.strptime(now, "%H:%M:%S")

        try:
            fromTime, toTime = self.fileTimeslot
        except InvalidTimePoint as err:
            # print(err)
            return False

        # Check if current time is in the given timeslot
        if currentWeekDay == self.fileWeekday and fromTime <= now <= toTime:
            return True
        else:
            return False



    @property
    def fileWeekday(self):
        """Guess the weekday from pathlib.Path object"""
        
        parentFolderName = self.fileObj.relative_to(self.rootFolder).parts[0]
        
        # Check weekday in parent folder name using regex
        if re.search(r"monday", parentFolderName, re.IGNORECASE):
            return "Monday"
        elif re.search(r"tuesday", parentFolderName, re.IGNORECASE):
            return "Tuesday"
        elif re.search(r"wednesday", parentFolderName, re.IGNORECASE):
            return "Wednesday"
        elif re.search(r"thursday", parentFolderName, re.IGNORECASE):
            return "Thursday"
        elif re.search(r"friday", parentFolderName, re.IGNORECASE):
            return "Friday"
        elif re.search(r"saturday", parentFolderName, re.IGNORECASE):
            return "Saturday"
        elif re.search(r"sunday", parentFolderName, re.IGNORECASE):
            return "Sunday"
        else:
            return None


    @property
    def fileTimeslot(self):
        """Guess the timeslot from pathlib.Path object"""
        
        parentFolderName = self.fileObj.relative_to(self.rootFolder).parts[1]
        
        # Extract from-time and to-time
        fromTo = re.findall(r"(\d{1,2}\.\d{2}\ ?[ap]m)", parentFolderName, re.IGNORECASE)
        if len(fromTo) != 2:
            raise InvalidTimePoint(f"Unable to parse fromTime and toTime - {self.fileObj}")

        # Add space between time and am/pm if needed
        fromTo = [re.sub(r"(\d{1,2}\.\d{2})([ap]m)", r"\1 \2", i, re.IGNORECASE) for i in fromTo]

        # Convert string to time-format
        fromTime = datetime.datetime.strptime(fromTo[0], "%I.%M %p")
        toTime = datetime.datetime.strptime(fromTo[1], "%I.%M %p")
        return fromTime, toTime


    def __str__(self):
        """Return string representation of MusicFile object"""
        return f'MusicFile obj of "{self.fileObj}")'