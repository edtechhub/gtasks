"""In charge of creating a backup of all Google Tasks on the current account."""
import os
import json

from gtasks import Gtasks


def backup():
    g = Gtasks()
    lists = g.get_lists()

    content = [_serialize_list(l) for l in lists]
    _backup_to_file(content)


def _serialize_list(task_list):
    # If we want completed/hidden tasks use `include_hidden=True`.
    # Can also get deleted tasks with `include_deleted=True`, but they are less interesting.
    list_of_tasks = _organize_tasks(task_list.get_tasks())

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
        "sub_tasks": [_serialize_task(sub_task) for sub_task in task.sub_tasks]
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


def _find_available_filename(filename):
    original_filename = filename.format("")
    if os.path.exists(original_filename):
        counter = 1

        incremented_filename = filename.format(counter)
        while os.path.exists(incremented_filename):
            counter += 1
            incremented_filename = filename.format(counter)
        return incremented_filename
    else:
        return original_filename


def _backup_to_file(backup_content):
    filename = _find_available_filename("backup{}.json")
    print("Creating backup in file: {}".format(filename))
    with open(filename, "w") as f:
        json.dump(backup_content, f, sort_keys=True, indent=4)
