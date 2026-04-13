class Task:
    date = None

    def __init__(self, id: int, status="incomplete", priority="low"):
        self.id = id
        self.setStatus(status)
        self.setPriority(priority)

    def updateTaskDetail(self, id, status, priority, taskName, subject):
        self.priority = priority
        self.subject = subject
        self.taskName = taskName
        self.status = status
        self.id = id

    # @brief This method returns the task details.
    # @param self
    # @return priority, subject, taskName, status, id

    def getTaskName(self):
        return self.taskName

    # @brief This method sets the priority of the task.
    # @param self, priority
    # @return None
    def setPriority(self, priority):
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Invalid priority")
        self.priority = priority

    def setStatus(self, status):
        if status not in ["complete", "incomplete"]:
            raise ValueError("Invalid status")
        self.status = status

    def newTask(self, subject, taskName):
        self.subject = subject
        self.taskName = taskName

    def setDate(self, date):
        self.date = date
