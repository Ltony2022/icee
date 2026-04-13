import time
from rich.progress import track
from rich.progress import Progress
import sys
import _thread


def input_thread(L):
    input()
    L.append(None)


def pomodoroInTerminal():
    L = []
    _thread.start_new_thread(input_thread, (L,))
    with Progress() as progress:
        task1 = progress.add_task("[red]Time left: ", total=25*60+1)
        while not progress.finished and not L:
            progress.update(task1, advance=1)
            time.sleep(1)
        if L:
            # print("\033c")
            print("Pomodoro timer has been stopped by user", file=sys.stderr)
            # If user choose to continue, then continue
            _thread.exit()