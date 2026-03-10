import json
import os

PROJECT_FILE = "current_project.json"


def start_project(goal):

    project = {
        "goal": goal,
        "steps": [],
        "completed": []
    }

    with open(PROJECT_FILE, "w") as f:
        json.dump(project, f)


def add_steps(steps):

    with open(PROJECT_FILE) as f:
        project = json.load(f)

    project["steps"] = steps

    with open(PROJECT_FILE, "w") as f:
        json.dump(project, f)


def get_project():

    if not os.path.exists(PROJECT_FILE):
        return None

    with open(PROJECT_FILE) as f:
        return json.load(f)