import sys
import os

# from typing import override
from interface.osCli import cli

home_screen = """\033[1;36mooooo  oooooooo8 ooooooooooo ooooooooooo 
 888 o888     88  888    88   888    88  
 888 888          888ooo8     888ooo8    
 888 888o     oo  888    oo   888    oo  
o888o 888oooo88  o888ooo8888 o888ooo8888 
                  
\033[1;33mICEE Alpha v0.1

1. Block Management
2. Pomodoro
3. Study Planner
4. Subject manager
5. Exit\033[1;33m\n"""


class windowsCli(cli):

    def __init__(self):
        print(home_screen)

    @staticmethod
    def clear_screen():
        return os.system("cls") if os.name == "nt" else os.system("clear")

    @staticmethod
    def block_options():
        windowsCli.clear_screen()
        print(
            """\033[1;33m1. Add block site
2. Remove block site
3. Enable block site
4. Disable block site
5. List blocked site
6. Return to the home page\033[1;33m\n"""
        )
        return "block_manager"

    @staticmethod
    def homepage():
        windowsCli.clear_screen()
        print(home_screen)
        return "homepage"
    @staticmethod
    def exit():
        sys.exit()
