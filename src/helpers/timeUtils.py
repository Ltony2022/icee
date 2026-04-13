"""
This is for adding the time support for the application
"""
from datetime import datetime
import time


def get_current_time():
    """
    This will return the current time
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date():
    """
    This will return the current date
    """
    return datetime.now().strftime("%d/%m/%Y")


def get_current_year():
    """
    This will return the current year
    """
    return datetime.now().strftime("%Y")

# Counting down the time


def countdown_timer(minutes: int):
    """
    This will count down the time
    """
    for i in range(minutes, 0, -1):
        print("Time left: ", i, " minutes")
        time.sleep(60)
    print("Time is up!")
    return True

# set date and time


def set_date_time():
    """
    This will set the date and time
    """
    # Ask user for the data
    date = input("Enter the date (YYYY-MM-DD): ")
    time = input("Enter the time (HH:MM:SS): ")
    return date, time


def calculateDateBetween(date1, date2):
    """
    This will calculate the date between two dates
    """
    date1 = datetime.strptime(date1, "%d/%m/%Y")
    date2 = datetime.strptime(date2, "%d/%m/%Y")
    return (date2 - date1).days
