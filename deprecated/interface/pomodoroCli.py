import tqdm
import time
from utils.pomodoroUtils import pomodoroUtils


def start():
    print("Welcome to the Pomodoro Timer!")
    print("What would you like to do?")
    print("1. Start a Pomodoro")
    print("2. Check the amount of Pomodoros completed")
    print("3. Exit")
    return "pomodoro"


def pomodoro_start():
    pomodoro = pomodoroUtils()
    print("Starting a Pomodoro!")
    for i in tqdm.tqdm(range(pomodoro.get_pomodoro_timer()*60)):
        time.sleep(1)
    print("Pomodoro Completed!")


def pomodoro_break():
    pomodoro = pomodoroUtils()
    print("Time for a break!")
    for i in tqdm.tqdm(range(pomodoro.breakTime())):
        time.sleep(60)
    print("Break Completed!")
