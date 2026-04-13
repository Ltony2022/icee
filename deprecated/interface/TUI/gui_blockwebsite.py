from textual.screen import Screen
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static


class startingSelection(Static):
    """The starting screen for the app."""

    def compose(self):
        """Create child widgets for the starting screen."""
        yield Static("Welcome to pomodoro timer")


class WebsiteBlocker(Screen):

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(startingSelection())
        yield Footer()
