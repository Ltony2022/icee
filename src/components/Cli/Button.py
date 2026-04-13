from textual.widgets import Button


class startButton(Button):
    """The button configuration."""

    def on_button_pressed(self):
        if self.id == "start":
            # Test if its working
            self.app.push_screen('actionMenu')
        elif self.id == "exit":
            self.app.exit()
        elif self.id == "back":
            self.app.pop_screen()


class mainButton(Button):
    # The button configuration for other screens
    menuMapper = {
        "blockwebsite": "blockWebsite",
        "studyplan": "studyPlanner",
        "pomodoro": "pomodoro",
        "websiteBlocker": "websiteBlocker",
        "studyPlanner": "studyPlanner"
    }

    def on_button_pressed(self):
        if self.id == "back":
            self.app.pop_screen()
        else:
            # get id from the button and map it to the screen
            nextScreen = self.menuMapper[self.id]
            self.app.push_screen(nextScreen)
