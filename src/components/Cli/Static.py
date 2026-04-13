from textual.widgets import Static

startScreen = """\033[1;36mooooo  oooooooo8 ooooooooooo ooooooooooo 
 888 o888     88  888    88   888    88  
 888 888          888ooo8     888ooo8    
 888 888o     oo  888    oo   888    oo  
o888o 888oooo88  o888ooo8888 o888ooo8888 
                  
\033[1;33mICEE Alpha v0.1\n"""


class headerView(Static):
    """The welcome screen for the app."""


class HeaderView(Static):
    """The welcome screen for the app."""

    def compose(self):
        yield headerView("Welcome to ICEE Alpha v0.1\n")
        # yield headerView("Welcome to ICEE Alpha v0.1\n")
        # yield headerView("A personal cultivated learning tool\n")
        # yield headerView("Developed by: ICEE Team\n")
        # yield headerView("For more information, visit https://www.icee.dev\n")
