from textual.screen import Screen
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static

from components.Cli.Button import mainButton as Button


class startingSelection(Static):
    """The starting screen for the app."""

    def compose(self):
        """Create child widgets for the starting screen."""
        yield Button("Block a website", id="websiteBlocker", variant="primary")
        yield Button("Study planner", id="studyplan", variant="primary")
        yield Button("Pomodoro", id="pomodoro", variant="default")
        yield Button("Back", id="back", variant="error")


class ActionMenu(Screen):

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(startingSelection())
        yield Footer()
