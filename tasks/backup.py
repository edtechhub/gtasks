"""In charge of creating a backup of all Google Tasks on the current account."""
from datetime import datetime
import json

from gtasks import Gtasks


def backup(include):
    if include == "all":
        include_hidden = True
    elif include == "visible":
        include_hidden = False
    else:
        include_hidden = True

    g = Gtasks()
    lists = g.get_lists()

    print(f"Including hidden tasks" if include_hidden else "Not including hidden tasks")
    content = []
    for l in lists:
        print(f"Adding list to backup: {l.title}")
        content.append(_serialize_list(l, include_hidden=include_hidden))
    _backup_to_file(content)


def _serialize_list(task_list, include_hidden=False):
    list_of_tasks = _organize_tasks(
        task_list.get_tasks(include_hidden=include_hidden, include_completed=include_hidden)
    )

    return {
        "id": task_list.id,
        "title": task_list.title,
        "updated": task_list._dict["updated"],
        "tasks": [_serialize_task(task) for task in list_of_tasks],
    }


def _serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "notes": task.notes,
        "updated": task._dict["updated"],
        "is_completed": task.complete,
        "sub_tasks": [_serialize_task(sub_task) for sub_task in task.sub_tasks],
        "links": task._dict.get("links", [])
    }


def _organize_tasks(tasks):
    """Shuffles a flat list of tasks into tasks that have a `sub_tasks` property."""
    parents = []
    orphans = []
    for task in tasks:
        task.sub_tasks = []
        if task.parent is None:
            parents.append(task)
        else:
            orphans.append(task)

    def _find_and_assign_task_to_parent(l, parent_id, task):
        for t in l:
            _find_and_assign_task_to_parent(t.sub_tasks, parent_id, task)
            if t.id == parent_id:
                t.sub_tasks.append(task)

    for task in orphans:
        parent_id = task.parent.id
        _find_and_assign_task_to_parent(parents, parent_id, task)

    return parents


def _backup_to_file(backup_content):
    now_string = datetime.now().isoformat()
    filename = f"backup-{now_string}.json"
    print("Creating backup in file: {}".format(filename))
    with open(filename, "w") as f:
        json.dump(backup_content, f, sort_keys=True, indent=4)
