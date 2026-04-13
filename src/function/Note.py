from src.helpers import timeUtils


class Note:
    def __init__(self):
        self.date = timeUtils.get_current_date()

    def setId(self, id):
        self.id = id

    def loadNoteDetails(self, title, content, date, id):
        self.title = title
        self.content = content
        self.date = date
        self.id = id

    def newNote(self, title, content):
        self.title = title
        self.content = content

    def getNoteDetails(self):
        return self.title, self.content, self.date, self.id
