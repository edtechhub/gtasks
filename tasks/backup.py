"""In charge of creating a backup of all Google Tasks on the current account."""
from datetime import datetime
import json
from unittest.mock import Mock
import traceback
from .gtask_wrapper import GTaskWrapper

# target_list: List to be backed up
# include: which tasks to include


def backup(target_list, include):
    if include == "all":
        include_hidden = True
    elif include == "visible":
        include_hidden = False
    print(f"Including hidden tasks" if include_hidden else "Not including hidden tasks")
    # if target_list is specified, then modify 'lists'
    g = GTaskWrapper()
    lists = g.get_lists(include_hidden)
    if target_list:
        original_count = len(lists)
        lists = [l for l in lists if l['title'].lower() == target_list.lower()]
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
            print(f"Adding list to backup: {l['title']}")
            unorganised_list_of_tasks = g.get_tasks(l['id'])
            content_unorganised = _serialize_list(l, unorganised_list_of_tasks)
            _backup_to_file("Unorganised_" + l['title'], content_unorganised)

            content = _serialize_list(
                l, _organize_tasks(unorganised_list_of_tasks))
            _backup_to_file("Organised_" + l['title'], content)
        except Exception:
            print('Failed to add list to backup: {}'.format(l['title']))
            traceback.print_exc()


def _serialize_list(task_list, list_of_tasks):
    return {
        "id": task_list['id'],
        "title": task_list['title'],
        "updated": task_list["updated"],
        "tasks": list_of_tasks
    }


def fake_task():
    t = {
        'id': "ghost",
        'title': "ghost",
        'notes': "ghost notes",
        'sub_tasks': [],
        "updated": "ghost"}
    return t


def _organize_tasks(tasks):
    """Shuffles a flat list of tasks into tasks that have a `sub_tasks` property."""
    task_map = {}
    for task in tasks:
        task_map[task['id']] = task

    ghost = fake_task()

    for task in tasks:
        parent_id = task.get('parent', None)
        if parent_id and task_map[parent_id]:
            if 'sub_tasks' not in task_map[parent_id]:
                task_map[parent_id]['sub_tasks'] = []
            task_map[parent_id]['sub_tasks'].append(task)
            del task_map[task['id']]
        elif parent_id:
            ghost['sub_tasks'].append(task)
            del task_map[task['id']]

    organized = []
    for _, value in task_map.items():
        organized.append(value)

    if len(ghost['sub_tasks']):
        organized.append(ghost)

    return organized


def _backup_to_file(file_name, backup_content):
    now_string = datetime.now().isoformat()
    filename = f"backup-{file_name}-{now_string}.json"
    print("Creating backup in file: {}".format(filename))
    with open(filename, "w") as f:
        json.dump(backup_content, f, sort_keys=True, indent=4)
