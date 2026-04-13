from re import sub
import uuid


class Subject():
    def __init__(self, courseCode=0, subjectName="", courseCurriculum=[], numberOfTopics=0):
        self.courseCode = courseCode
        self.subjectName = subjectName
        self.courseCurriculum = courseCurriculum
        #! Might be migrated to private
        self.numberOfTopics = numberOfTopics

    def createNewSubject(self):
        # Automatically creating the id
        self.id = input("Enter the course ID: ")
        self.subjectName = input("Enter your subject name: ")
        # self.topic = input("Enter your topic: ")
        # there can be multiple topics within the app
        # perhaps just ask for the number of topics for now
        self.numberOfTopics = int(input("Enter the number of topics: "))
