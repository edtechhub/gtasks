from gtasks import Gtasks

from .backup import _organize_tasks


def process(target_list, match):
    list_ = _find_list_with_name(target_list)

    if list_ is None:
        return

    print("List: ", list_.title)

    tasks = list_.get_tasks()
    tasks = _organize_tasks(tasks)

    if match is not None:
        print("Filtering tasks by term: ", match)
        tasks = _filter_tasks(tasks, match)

    if not tasks:
        print("Did not find any tasks to list!")
    for i, t in enumerate(tasks):
        print("--")
        print(f"Task {i}")
        _print_task(t)
    print()

    print("Done processing!")


def _find_list_with_name(name):
    """Returns single list that matched if we found a match, or None if it's not sure.
    Will print debug info if not found.
    """
    g = Gtasks()
    lists = g.get_lists()

    available_list_names = [l.title for l in lists]
    matching_lists = [l for l in lists if l.title.lower() == name.lower()]
    if len(matching_lists) > 1:
        print(f"Found {len(matching_lists)} lists that match name, not sure which to use: {name}")
        return None

    if len(matching_lists) == 0:
        print(f"Could not find any lists that match that name: {name}")
        print("Available list names:")
        print(", ".join(available_list_names))
        return None

    return matching_lists[0]


def _print_task(task):
    """Includes any sub_tasks it has."""
    print("Title: ", task.title)
    print("Description: ", task.notes)
    print("Last Updated: ", task._dict["updated"])
    if task.sub_tasks:
        print("Sub Tasks:")
        indent = " " * 4
        for sub_task in task.sub_tasks:
            print(f"{indent}--")
            print(f"{indent}Title: ", sub_task.title)
            print(f"{indent}Description: ", sub_task.notes)
            print(f"{indent}Last Updated: ", sub_task._dict["updated"])


def _filter_tasks(tasks, match):
    """Filter out tasks based on title and description for the given string.

    If a parent doesn't match, the subtasks are ignored.
    """
    def is_match(task, term):
        return term in task.title.lower() or (task.notes and term in task.notes.lower())

    match = match.lower()
    tasks = [t for t in tasks if is_match(t, match)]
    for t in tasks:
        t.sub_tasks = [t for t in t.sub_tasks if is_match(t, match)]

    return tasks
