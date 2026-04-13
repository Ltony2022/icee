from src.function.StudyPlanner import StudyPlanner

# from src.controller.windowsController import study_planner_action

study_planner = StudyPlanner()


def test_createPlan():
    planner = (
        planName := "plan1",
        startDate := "01/02/2023",
        endDate := "10/02/2023",
        tasks := [
            {"taskName": "task1", "subject": "subject1"},
            {"taskName": "task2", "subject": "subject1"}
        ],
    )
    study_planner.createPlan(planner)


def test_study_planner():
    # createPlan()
    global study_planner
    # Create a new study planner
    test_createPlan()
    # create object with properties
    info = study_planner.getPlannerData()
    # Get the study planner
    assert info["plan1"] == [
        "10/02/2023",
        [{"id": 0, "taskName": "task1", "status": "incomplete", "subject": "subject1", "priority": "low", "date": None},
         {"id": 1, "taskName": "task2", "status": "incomplete", "subject": "subject1", "priority": "low", "date": None}]
    ]


def test_calculate_effort_per_day():
    global study_planner
    # Calculate the effort per day (2 tasks `task1` and `task2` in 3 days)
    effort_per_day = study_planner.suggest_calculateEffortPerDay("01/02/2023", "03/02/2023", [
        {"taskName": "task1", "subject": "subject1"},
        {"taskName": "task2", "subject": "subject1"}
    ])
    assert effort_per_day == 1


def test_suggest_splitting_task():
    global study_planner
    # test_newStudyPlanner()
    test_createPlan()
    # Suggest splitting the task based on the date
    days_left = 3
    study_planner.distributeTasksByDate(
        days_left, study_planner.listOfPlans["plan1"][1])
    info = study_planner.getPlannerData()
    # Get the study planner
    assert info["plan1"] == [
        "10/02/2023", [{"id": 0, "taskName": "task1", "status": "incomplete", "subject": "subject1", "priority": "low",
                        "date": "01/02/2023"},
                       {"id": 1, "taskName": "task2", "status": "incomplete", "subject": "subject1", "priority": "low",
                        "date": "02/02/2023"}]]
