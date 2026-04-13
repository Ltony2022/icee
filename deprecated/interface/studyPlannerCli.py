from sqlite3 import Date
from function.StudyPlanner import StudyPlanner
from datetime import datetime


def start(verbose=True):
    print("Starting the planner...")
    print("Welcome to study planner")
    print("1. Create a plan")
    print("2. View today's plan")
    print("3. View plan")
    print("4. Update plan")
    print("5. Return to the home page")
    if verbose:
        print("=====================================")
        print("Verbose mode is on")
        print("6. Preload sample data")
        print("=====================================")
    return "study_planner"


# def isCustomOrAuto():
#     print("Do you want to create a custom plan or auto plan?")
#     print("1. Custom plan")
#     print("2. Auto plan")
#     return input("Enter the number: ")


def create_plan():
    planName = input("Enter the name of the plan: ")
    startDate = input(
        "Enter the start date of the plan(in format dd/mm/yyyy): ")
    endDate = input("Enter the end date of the plan(in format dd/mm/yyyy): ")
    tasks: list = []
    while True:
        task = input("Enter the task name: ")
        subject = input("Enter the subject of the task: ")
        tasks.append({"taskName": task, "subject": subject})
        if input("Do you want to add another task? (y/n) ") != "y" or "Y":
            break
    checkBeforeCreating(planName, startDate, endDate, tasks)
    return planName, startDate, endDate, tasks


def checkBeforeCreating(planName, startDate, endDate, tasks):
    # Check if the date format is correct
    startDateConversion = datetime.strptime(startDate, "%d/%m/%Y")
    endDateConversion = datetime.strptime(endDate, "%d/%m/%Y")
    dateFormat = startDateConversion.strftime("%d/%m/%Y")
    if startDate != dateFormat or endDate != dateFormat:
        raise ValueError("Invalid date format")

    # Check if the end date is greater than the start date
    if startDateConversion > endDateConversion:
        raise ValueError("End date cannot be less than the start date")


def today_plan(studyPlannerObj: StudyPlanner):
    print("Today's task list: ")
    unfilteredData = studyPlannerObj.getPlannerData()
    # Filter out the task for today if matches the date
    today = datetime.now().strftime("%d/%m/%Y")
    filter_today_tasks(unfilteredData, today)


def view_plan(studyPlannerObj):
    planner = studyPlannerObj.getPlannerData()
    for planKey in planner:
        print(f"Plan name: {planKey}")
        taskList = planner[planKey]
        for taskIndex in range(0, len(taskList)):
            displayTaskInformation(taskList, taskIndex)


def update_plan():
    # print("Here is the list of the task for today: ")
    pass


def displayTaskInformation(taskList, taskIndex):
    print(f"Task name: {taskList[1][taskIndex]['taskName']}")
    print(f"Task status: {taskList[1][taskIndex]['status']}")
    print(f"Task priority: {taskList[1][taskIndex]['priority']}")
    print(f"Task subject: {taskList[1][taskIndex]['subject']}")


def filter_today_tasks(unfilteredData: dict[str, list], today: datetime):
    if len(unfilteredData) == 0:
        print("No task for today")
        return
    for planKey in unfilteredData:
        taskList = unfilteredData[planKey]
        taskCount = len(taskList)
        todayTask = 0
        # Task Count = 0 means no task for today
        if taskCount == 0:
            print("No task available")
            return
        for taskIndex in range(0, taskCount):
            taskDate = taskList[1][taskIndex]['date']
            if taskDate == today:
                displayTaskInformation(taskList, taskIndex)
                todayTask += 1
        if todayTask == 0:
            print("No task for today")


def update_plan():
    print(
        "(Error: This feature is only available in the GUI version of the application)"
    )
