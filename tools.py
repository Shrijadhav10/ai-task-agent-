import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task: str):
    tasks = load_tasks()
    tasks.append({"task": task, "completed": False})
    save_tasks(tasks)
    return f"Task added: {task}"

def get_tasks():
    tasks = load_tasks()
    return tasks

def delete_task(task: str):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["task"] != task]
    save_tasks(tasks)
    return f"Deleted: {task}"

def mark_complete(task: str):
    tasks = load_tasks()
    for t in tasks:
        if t["task"] == task:
            t["completed"] = True
    save_tasks(tasks)
    return f"Marked as completed: {task}"

def clear_tasks():
    save_tasks([])
    return "All tasks cleared."
