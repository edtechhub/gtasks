"""In charge of creating a backup of all Google Tasks on the current account."""
from gtasks import Gtasks


def backup():
    # Find all the tasks. (Do I want completed ones?)
    # Loop through them and store.

    # Need a structure for the nested tasks.
    g = Gtasks()
    lists = g.get_lists()

    print("Have the lists: ", lists)
    content = [_serialize_list(l) for l in lists]
    _backup_to_file(content)


def _serialize_list(list):
    print("Backing up list")
    # Group them so that they have sub_tasks now, instead of being flat.
    tasks = _serialize_tasks()
    return {
        "name": "test",
        "tasks": tasks,
    }


def _serialize_tasks():
    return []


def _serialize_task(task):
    return {}


def _organize_children(tasks):
    # Might need this for the `process` as well, so might need to move somewhere else.
    parents = []
    orphans = []
    for task in tasks:
        task.sub_tasks = []
        if task.parent is None:
            parents.append(task)
        else:
            print("Task is orphan!")
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


def _backup_to_file(backup_content_dict):
    # Convert to jsonstring.
    # Write to file.
    # Probably a fixed file at this stage, and not letting the user choose.
    pass
