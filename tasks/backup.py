"""In charge of creating a backup of all Google Tasks on the current account."""
from datetime import datetime
import json
from unittest.mock import Mock
import traceback
from gtasks import Gtasks

# target_list: List to be backed up
# include: which tasks to include


def backup(target_list, include):
    if include == "all":
        include_hidden = True
    elif include == "visible":
        include_hidden = False
    print(f"Including hidden tasks" if include_hidden else "Not including hidden tasks")
    # if target_list is specified, then modify 'lists'
    g = Gtasks()
    lists = g.get_lists()
    if target_list:
        original_count = len(lists)
        lists = [l for l in lists if l.title.lower() == target_list.lower()]
        new_count = len(lists)
        if not lists:
            print(
                f"Could not find any lists with the name '{target_list}' to backup!")
            return
        else:
            print(f"Backing up {new_count} of {original_count} lists.")

    # Lists now contains either all lists or the targeted lists
    # Get content for each list.new_count} of {original_count} lists.")
    for l in lists:
        try:
            print(f"Adding list to backup: {l.title}")
            unorganised_list_of_tasks = l.get_tasks(include_hidden=include_hidden,
                                                    include_completed=include_hidden)
            content_unorganised = _serialize_list(l, unorganised_list_of_tasks)
            _backup_to_file("Unorganised_"+l.title, content_unorganised)
            content = _serialize_list(
                _organize_tasks(l, unorganised_list_of_tasks))
            _backup_to_file("Organised_"+l.title, content)
        except Exception:
            print('Failed to add list to backup: {}'.format(l.title))
            traceback.print_exc()


def _serialize_list(task_list, list_of_tasks):
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
        "links": task._dict.get("links", []),
        "due": task._dict.get("due")
    }


def fake_task():
    t = Mock()
    t.id = "ghost"
    t.title = "ghost"
    t.notes = "ghost notes"
    t.complete = False
    t.sub_tasks = []

    t._dict = {"updated": "ghost"}
    return t


def _organize_tasks(tasks):
    """Shuffles a flat list of tasks into tasks that have a `sub_tasks` property."""
    parents = []
    children = []

    ghost = fake_task()
    #orphanage = fake_task()

    for task in tasks:
        task.sub_tasks = []
        try:
            if task.parent is None:
                parents.append(task)
            else:
                children.append(task)
        except Exception:
            print(
                f"Got error trying to find parent for task with ID: {task.id}, Title: {task.title}. Adding to ghost task.")
            ghost.sub_tasks.append(task)

    for task in children:
        try:
            parent = task.parent
            _find_and_assign_task_to_parent(parent, task)
        except Exception:
            print('FATAL ERROR: Could not find parent for {}'.format(task.title))
            # orphanage.sub_tasks.append(task)

    if ghost.sub_tasks:
        parents.append(ghost)

    return parents


def _find_and_assign_task_to_parent(parent, task):
    parent.sub_tasks.append(task)
    if parent.parent:
        _find_and_assign_task_to_parent(parent.parent, parent)
    # for t in l:
    #     _find_and_assign_task_to_parent(t.sub_tasks, parent_id, task)
    #     if t.id == parent_id:
    #         t.sub_tasks.append(task)


def _backup_to_file(file_name, backup_content):
    now_string = datetime.now().isoformat()
    filename = f"backup-{file_name}-{now_string}.json"
    print("Creating backup in file: {}".format(filename))
    with open(filename, "w") as f:
        json.dump(backup_content, f, sort_keys=True, indent=4)
