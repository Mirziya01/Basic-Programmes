import json
import argparse
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    if TASKS_FILE.stat().st_size == 0:
        return []

    with open(TASKS_FILE, "r") as f:
        return json.load(f)



def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title):
    tasks = load_tasks()
    next_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({
        "id": next_id,
        "title": title,
        "done": False
    })
    save_tasks(tasks)
    print(f"Added task #{next_id}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['title']}")

def mark_done(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task #{task_id} as done")
            return

    print(f"No task found with id {task_id}")

def delete_task(task_id):
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Deleted task #{task_id}")
            return

    print(f"No task found with id {task_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Simple terminal task manager"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs = "+",help="Task title")

    # list command
    subparsers.add_parser("list", help="List all tasks")

    # done command
    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")


    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.title))
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "delete":
        delete_task(args.id)




if __name__ == "__main__":
    main()
