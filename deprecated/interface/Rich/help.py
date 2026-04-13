from rich import print
from rich.panel import Panel
from rich.padding import Padding
from constant.listOfSupportedArgs import supportedArgs


def help(arg: str = None):
    # Get the help for the argument
    helpCommand = supportedArgs.get(arg[0])
    # definitionFormat = Padding(helpCommand, 10)
    # print(definitionFormat)
    content = f"--[blue]{arg[0]}[/blue]:\t\t\t{helpCommand}"
    print(Panel(
        f"Welcome to ICEE-utils [red]console[/red] edition! \n{content}", title="Help"))
# import sys

# sys.argv[1:]
