from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static, Footer, Header

# from interface.components.cli.Button import actionButton

# Own imports
from components.Cli.Static import HeaderView
from components.Cli.Button import startButton
from function.StudyPlanner import StudyPlanner

from interface.TUI.gui_actionMenu import ActionMenu
from interface.TUI.gui_pomodoro import PomodoroTimer
from interface.TUI.gui_blockwebsite import WebsiteBlocker


class startingSelection(Static):
    """The starting screen for the app."""

    def compose(self):
        """Create child widgets for the starting screen."""
        yield startButton("Start", id="start", variant="primary")
        # todo: exit app action
        yield startButton("About", id="about", variant="default")
        yield startButton("Exit", id="exit", variant="error")


class ICEEApp(App):
    is_running = True
    """A Textual app for all-in-one personal cultivated learning tools."""
    CSS_PATH = "./public/tcss/welcome.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    SCREENS = {"actionMenu": ActionMenu,
               "pomodoro": PomodoroTimer,
               "websiteBlocker": WebsiteBlocker,
               "studyPlanner": StudyPlanner}

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield HeaderView()
        yield ScrollableContainer(startingSelection())
        yield Footer()

    # def on_mount(self) -> None:
    #     """Mount the app."""
    #     self.install_screen('actionMenu', ActionMenu())


if __name__ == "__main__":
    app = ICEEApp()
    app.run()
    if app.is_running:
        app.exit()
