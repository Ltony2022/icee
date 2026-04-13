class pomodoroUtils:
    # Variables include the time for the pomodoro, the short break, and the long break
    pomodoro_time = 25
    short_break = 5
    long_break = 15
    amount_of_pomodoros = 0

    def __init__(self):
        pass

    def get_pomodoro_timer(self):
        return self.pomodoro_time

    def startPomodoro(self):
        self.amount_of_pomodoros += 1
        return self.pomodoro_time

    def breakTime(self):
        if self.amount_of_pomodoros % 4 == 0:
            return self.long_break
        else:
            return self.short_break

    def check_pomodoro(self):
        return self.amount_of_pomodoros