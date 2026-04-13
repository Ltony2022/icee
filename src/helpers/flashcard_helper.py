# Modify the flashcard creation to include the default
# params set in SM2 algorithm

# May possibly support bring-your-own-algorithm
from datetime import datetime


class FlashcardHelper:
    # Possibly having a user configuration for modifying the default params
    def __init__(self):
        self.default_EFactor = 2.5
        self.default_interval = 1
        self.default_repetition = 1
        self.next_practice = datetime.now()

    def init_flashcard(self, data):
        # Default params variables
        EFactor = self.default_EFactor
        interval = self.default_interval
        repetition = self.default_repetition
        nextPractice = self.next_practice

        # add the default params to the data
        data['EFactor'] = EFactor
        data['interval'] = interval
        data['repetition'] = repetition
        data['nextPractice'] = nextPractice
        return data
