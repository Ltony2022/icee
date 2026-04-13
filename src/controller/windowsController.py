# !@brief { This class is for the subject interface in the command line interface }
# ---------------------------------
# 1. Interface
from interface import pomodoroCli
from interface import studyPlannerCli
from interface import subjectCli
from interface.windowsCli import windowsCli
from interface.studyPlannerCli import *
from interface.pomodoroCli import *
from interface.subjectCli import *

# ---------------------------------
# 2. Utilities
from utils.WindowsBlockUtils import WindowsBlockUtils

# ---------------------------------
# 3. Function
from function.StudyPlanner import StudyPlanner
from function.Subject import Subject

# ---------------------------------

# Initialize the windows block utils
windows_block_utils = WindowsBlockUtils()
study_planner = StudyPlanner()

# Action for the block manager
dict_block_manager = {
    "1": windows_block_utils.add_block_site,
    "2": windows_block_utils.remove_block_site,
    "3": windows_block_utils.enable_block_site,
    "4": windows_block_utils.disable_block_site,
    "5": windows_block_utils.list_block_sites,
    "6": windowsCli.homepage,
}

dict_block_action = {
    "1": lambda: input("Enter the website to block: "),
    "2": lambda: input("Enter the website to unblock: "),
    "3": lambda: input("Enter the website to enable: "),
    "4": lambda: input("Enter the website to disable: "),
}

# Action for the pomodoro
dict_pomodoro_manager = {
    "1": pomodoroCli.pomodoro_start,
    # "2": pomodoroCli.check_pomodoro,
    "3": windowsCli.homepage,
}

# Action for the note manager
dict_note_manager = {}


# Action for the study planner
study_planner_interface_list = {
    "1": lambda: studyPlannerCli.create_plan,
    "2": studyPlannerCli.today_plan,
    "3": studyPlannerCli.view_plan,
    "4": studyPlannerCli.update_plan,
    "5": windowsCli.homepage,
}

study_planner_action = {
    "1": study_planner.createPlan,
}

study_planner_verbose = {
    "6": study_planner.verbose_loadData,
}

# Action for the subject manager
subjectManagerInterface = {
    "1": subjectCli.start,
    "2": subjectCli.start,
    "3": subjectCli.start,
    "4": windowsCli.homepage,
}


class WindowsController:
    def __init__(self):
        windowsCli()
        # Configurable options
        self.blockcontroller = BlockController()
        self.pomodorocontroller = PomodoroController()
        self.studyplannercontroller = StudyPlannerController()
        self.subjectcontroller = subjectManagerController()
        self.current_screen = "homepage"
        self.dict_home_screen = {
            "1": windowsCli.block_options,
            "2": pomodoroCli.start,
            "3": studyPlannerCli.start,
            "4": subjectCli.start,
            "5": windowsCli.exit,
        }
        # TODO: implement verbose mode
        self.verbose = False

        while True:
            self.inp = input("icee>")
            # Wait for the user to input something

            if self.current_screen == "homepage":
                self.routingUser()
            elif self.current_screen == "block_manager":
                self.blockcontroller.blockOperation(self)
            elif self.current_screen == "pomodoro":
                self.pomodorocontroller.pomodoroOperation(self)
            elif self.current_screen == "study_planner":
                self.studyplannercontroller.routingUser(self)
            elif self.current_screen == "subject_manager":
                self.subjectcontroller.subjectOperation(self)

    def getCurrentScreen(self):
        return self.current_screen

    def getInput(self):
        return self.inp

    def routingUser(self):
        if self.current_screen == "homepage":
            if self.inp in self.dict_home_screen:
                self.current_screen = self.dict_home_screen[self.inp]()
            else:
                print("Invalid input")


class BlockController(WindowsController):
    global windows_block_utils
    # global dict_block_manager
    # global dict_block_action

    def __init__(self) -> None:
        # pass the super class
        self.block_utils = windows_block_utils

    def blockOperation(self, controller: WindowsController):
        currentScreen = controller.getCurrentScreen()
        userInput = controller.getInput()
        print("Current screen: ", currentScreen)
        if currentScreen == "block_manager":
            if userInput in dict_block_manager and int(userInput) in range(1, 5):
                trackingWebsite = dict_block_action[userInput]()
                dict_block_manager[userInput](trackingWebsite)
            elif int(userInput) in range(5, 7):
                dict_block_manager[userInput]()
            else:
                print("Invalid input")


class PomodoroController(WindowsController):
    def __init__(self) -> None:
        pass

    def pomodoroOperation(self, controller: WindowsController):
        if controller.getCurrentScreen() == "pomodoro":
            if controller.getInput() in dict_pomodoro_manager:
                dict_pomodoro_manager[controller.getInput()]()
            else:
                print("Invalid input")


class StudyPlannerController(WindowsController):
    # Initialize the study planner for this class
    global study_planner

    def __init__(self):
        # Importing data (tasks, subjects, etc.)
        # Import all
        # For now just pass
        pass

    def routingUser(self):
        userInput = super().getInput()
        currentScreen = super().getCurrentScreen()
        if currentScreen == "study_planner":
            if userInput == "1":
                planner = study_planner_interface_list[userInput]()
                study_planner_action[userInput](planner)
            elif userInput in study_planner_interface_list:
                # Access the interface via input
                study_planner_interface_list[userInput](study_planner)
            elif userInput in study_planner_verbose:
                study_planner_verbose[userInput]()
            else:
                print("Invalid input")


class subjectManagerController(WindowsController):

    def __init__(self):
        # 1. Subject action logic
        self.subjectManagerLogic = {
            "1": lambda: self.createSubject(),
            "2": lambda: input("Enter the subject name: "),
            "3": lambda: input("Enter the subject name: "),
        }
        self.subjects = []

    def subjectOperation(self, controller: WindowsController):
        userInput = controller.getInput()
        currentScreen = controller.getCurrentScreen()
        subjectManagerInterface = self.dict_subject_manager
        userAction = self.subjectManagerLogic

        if currentScreen == "subject_manager":
            if userInput in userAction:
                userAction[userInput]()
            else:
                print("Invalid input")

    def createSubject(self):
        newSubject = Subject()
        newSubject.createNewSubject()
        self.subjects.append(newSubject)
        print("Subject created!")

    def editSubject(self):
        print("You found an easter egg! This feature is not yet implemented.")
