__all__ = ["windowsController"]

from core import osinfo
from windowsController import WindowsController


class Controller:
    operating_system = ""

    def __init__(self) -> None:
        pass

    # Library to get the OS

    # Importing controller

    def show_cli(self) -> None:
        self.operating_system = osinfo.check_system()
        if self.operating_system == "Windows":
            WindowsController()
