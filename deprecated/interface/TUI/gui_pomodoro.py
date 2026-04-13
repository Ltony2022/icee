from time import monotonic
from textual.screen import Screen
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static, Button
from textual.reactive import reactive


class TimeDisplay(Static):
    """A widget to display elapsed time."""
    pomodoroFixedTime = 25 * 60
    # Variable times
    prevElapsedTime = reactive(0.0)
    time = reactive(pomodoroFixedTime)
    elapsedTime = reactive(0.0)
    lastCheckpoint = reactive(0.0)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        if (time <= 0):
            self.stop()
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def on_mount(self) -> None:
        """Method called when the widget is mounted."""
        # Update time every 1/60th of a second
        self.update_timer = self.set_interval(
            1 / 60, self.updateTime, pause=True)

    def updateTime(self) -> None:
        """Method to update the time to the current time."""
        # Minus because we need to start fresh
        # due to the monotonic() function getting the current time
        currentProgress = monotonic() - self.lastCheckpoint
        # then we will reintroduce the previous elapsed time
        self.elapsedTime = currentProgress + self.prevElapsedTime
        self.time = self.pomodoroFixedTime - self.elapsedTime

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        # Initialize the last checkpoint
        self.lastCheckpoint = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.prevElapsedTime = self.elapsedTime
        self.time = self.pomodoroFixedTime - self.elapsedTime

        # self.time = self.startTime - self.elapsedTime

    def reset(self) -> None:
        """Method to reset the time display to 25 minutes."""
        self.lastCheckpoint = 0.0
        self.elapsedTime = 0.0
        self.time = self.pomodoroFixedTime
        self.prevElapsedTime = 0.0


class IndividualPomodoros(Static):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self):
        """Create child widgets of a pomodoro."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()


class Body(Static):
    """The starting screen for the app."""

    def compose(self):
        """Create child widgets for the starting screen."""
        yield Static("Welcome to pomodoro timer")
        yield Static("Press start to begin a pomodoro")


class PomodoroTimer(Screen):
    CSS_PATH = "../../public/tcss/pomodoro.tcss"

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        yield Body()
        yield ScrollableContainer(IndividualPomodoros())
        yield Footer()
