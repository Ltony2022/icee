from utils.timeUtils import *


class DateAndTime:
    def __init__(self):
        self.time = get_current_time()
        self.date = get_current_date()

    def set_date_and_time(self):
        """
        This will set the date and time
        """
        # Ask user for the data
        self.time = set_date_time()[0]
        self.date = set_date_time()[1]

    def get_date_and_time(self):
        """
        This will return the current date and time
        """
        return self.date, self.time
