"""!@brief {this class is for the subject interface in the command line interface}
"""


from function.Subject import Subject


def start():
    print("Starting the subject interface...")
    print("Welcome to the subject manager!")
    print("What you want to do?")
    print("1. Add a subject")
    print("2. Edit a subject")
    print("3. Remove a subject")
    print("4. Back to the homepage")
    return "subject_manager"


def displayOneSubject(subject: Subject):
    print("Subject name: " + subject.subjectName)
    print("Topic: " + subject.topic)
