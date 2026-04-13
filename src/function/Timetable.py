"""!@package Timetable
This module contains the class for the timetable.

"""

class timeTableGrid():
    def __init__(self):
        self.column = 96
        self.row = 7
        
    def print_timetable(self):
        print("TimeTable")
        for i in range(self.row):
            for j in range(self.column/4):
                print("-", end = "")
            print()
        