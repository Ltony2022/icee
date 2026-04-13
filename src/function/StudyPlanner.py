import math
from datetime import datetime, timedelta

from src.function.Task import Task
from src.helpers.timeUtils import calculateDateBetween

"""!@brief This is a class for the study planner.
"""


class StudyPlanner:

    def __init__(self):
        self.listOfPlans = {}
        self.status = "incomplete"
        self.daysLeft = 0
        self.streak = 0
        self.daysPerformed = 0
        # !! will be changed in production
        self.verbose = True

    def suggest_calculateEffortPerDay(self, startDate, endDate, tasks, reserved=0):
        # Days for reserve / revision
        daysForReserve = reserved
        # Amount of task
        amountOfTasks = len(tasks)
        verbose = self.verbose
        # Calculate the days left
        if verbose == True:
            print("[studyplanner] Calculating effort per day...")
        startDateConversion = datetime.strptime(startDate, "%d/%m/%Y")
        endDateConversion = datetime.strptime(endDate, "%d/%m/%Y")
        # Calculate the days left
        daysLeft = (endDateConversion - startDateConversion).days
        # Calculate the effort per day (round up if there is a remainder and its 0.5)
        effortPerDay = math.ceil(amountOfTasks / (daysLeft - daysForReserve))
        if (effortPerDay == 0 and amountOfTasks > 0) or (
                effortPerDay == 0 and daysLeft == 0
        ):
            effortPerDay = amountOfTasks
        if verbose == True:
            print("[studyplanner] Effort per day: ", effortPerDay)
        return effortPerDay

    def createPlan(self, planner):
        verbose = self.verbose
        # Set the date and the tasks
        # endDate, tasks, planName = planner
        planName, startDate, endDate, tasks = planner

        self.setEndDate(endDate)
        self.setStartDate(startDate)
        # calculate days left
        self.daysLeft = calculateDateBetween(self.startDate, self.endDate)
        # Create a plan that has end date and tasks
        if verbose == True:
            print("[studyplanner] Creating plan...")
        self.updatePlan(endDate, tasks, planName)
        # self.distributeTasks()
        # Split the task based on the date

    def updatePlan(self, date, tasks, planName):
        # Convert raw text tasks to task objects (logic will be imp later on)
        bufferedTasks = []
        # this id is for testing purposes
        id = 0
        # Every task is a dictionary
        for singletask in tasks:
            # New object
            task = Task(id)
            task.newTask(singletask["subject"], singletask["taskName"])
            # Append to the buffer
            bufferedTasks.append(task)
            id += 1
        # Distribute the tasks
        tasks = self.splitTasks(bufferedTasks)
        # Add instance to the dictionary
        finalData = [date, tasks]
        # [task[0].getTask() for task in tasks_buffer]
        self.listOfPlans[planName] = finalData

    """!@brief This method returns the plan details.
    @param self
    @return plan details
    """

    def splitTasks(self, tasks):
        daysLeft = self.daysLeft
        verbose = self.verbose
        if daysLeft < 0:
            raise ValueError("Invalid date")
        tasksperDay = self.suggest_calculateEffortPerDay(
            self.startDate, self.endDate, tasks
        )
        i = 0
        date = self.startDate
        for task in tasks:
            if verbose == True:
                print("[studyplanner] Current date: ", date)
                print("[studyplanner] i: ", i)
            if i == tasksperDay:
                i = 0
                date = self.incrementDate(date)
                if verbose == True:
                    print("[studyplanner] Incrementing date to: ", date)
            task.setDate(date)
            i += 1
        return tasks

    def incrementDate(self, date):
        # If the date format is not dd/mm/yyyy, then throw an error
        dateConversion = datetime.strptime(date, "%d/%m/%Y")
        dateFormat = dateConversion.strftime("%d/%m/%Y")
        if date != dateFormat:
            raise ValueError("Invalid date format")
        dateConversion = dateConversion + timedelta(days=1)
        return dateConversion.strftime("%d/%m/%Y")

    def getPlannerData(self):
        """This method returns the plan details.

        Returns:
            assertionData: dictionary of the plan details for other class to use.
        """
        assertionData = {}
        for plan in self.listOfPlans.items():
            taskArray = []
            planName = plan[0]
            date = plan[1][0]
            # There are many tasks in the plan
            taskList = plan[1][1]
            for task in taskList:
                tasks = self.extractTask(task)  # will output a dictionary
                taskArray.append(tasks)
            assertionData[planName] = [date, taskArray]
        return assertionData

    def extractTask(self, task):
        """!@brief This method extracts the task details.

        Args:
            task (Task): The task object.

        Returns:
            Dict[str, str]: The task details.(in form of dictionary)
        """
        if isinstance(task, Task):
            taskName = task.taskName
            subject = task.subject
            status = task.status
            priority = task.priority
            date = task.date
            id = task.id
            return {
                "id": id,
                "taskName": taskName,
                "status": status,
                "subject": subject,
                "priority": priority,
                "date": date,
            }
        else:
            raise ValueError("Invalid task object")

    def setEndDate(self, date):
        # If the date format is not dd/mm/yyyy, then throw an error
        dateConversion = datetime.strptime(date, "%d/%m/%Y")
        dateFormat = dateConversion.strftime("%d/%m/%Y")
        if date != dateFormat:
            raise ValueError("Invalid date format")
        self.endDate = date

    def setStartDate(self, date):
        # If the date format is not dd/mm/yyyy, then throw an error
        dateConversion = datetime.strptime(date, "%d/%m/%Y")
        dateFormat = dateConversion.strftime("%d/%m/%Y")
        if date != dateFormat:
            raise ValueError("Invalid date format")
        self.startDate = date

    # Verbose mode only
    # 1. add data

    def verbose_loadData(self):
        print("[studyplanner] Testing creating plan...")
        self.verbose_presetData()
        print("[studyplanner] Plan created")

    def verbose_presetData(self):
        plannerData = (
            planName := "plan1",
            startDate := "14/02/2024",
            endDate := "18/02/2024",
            tasks := [
                {"taskName": "task1", "subject": "subject1"},
                {"taskName": "task2", "subject": "subject1"},
            ],
        )
        self.createPlan(plannerData)
