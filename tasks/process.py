import json
import subprocess

from gtasks import Gtasks

from .backup import _organize_tasks, _serialize_task


def process(
    target_list,
    match,
    interactive,
    action,
    pipeto,
    pipe_separately="no",
    match_mode="default"
):
    print()

    interactive = True if interactive == "yes" else False
    pipe_separately = True if pipe_separately == "yes" else False

    list_ = _find_list_with_name(target_list)

    if list_ is None:
        return

    print("List: ", list_.title)

    tasks = list_.get_tasks(include_completed=False)
    tasks = _organize_tasks(tasks)

    if match is not None:
        print("Filtering tasks by term: ", match)
        tasks = _filter_tasks(tasks, match, match_strategy)

    if not tasks:
        print("Did not find any tasks!")

    actionator = Actionator(action)
    piper = Piper(pipeto) if pipeto else None

    if interactive:
        _interactive(tasks, actionator, piper)
    else:
        _non_interactive(tasks, actionator, piper, pipe_separately)

    print("Done processing!")


def _interactive(tasks, actionator, piper):
    for i, t in enumerate(tasks):
        print("--")
        print(f"Task {i}")
        _print_single_task(t, ignore_sub_tasks=True)
        if t.sub_tasks:
            print("Number of Sub Tasks:", len(t.sub_tasks))

        answer = _present_options(t, actionator, piper)
        print()

        if answer == "e":
            for sub in t.sub_tasks:
                print("--")
                print(f"Task {i}")
                _print_single_task(sub, ignore_sub_tasks=True)
                answer = _present_options(sub, piper)
                if answer == "y":
                    content = _serialize_task(sub)
                    piper.pipe(content)
                    actionator.take_action(sub)
                elif answer == "n":
                    pass
        elif answer == "y":
            content = _serialize_task(t)
            if piper:
                piper.pipe(content)
            actionator.take_action(t)
        elif answer == "n":
            pass


def _present_options(task, actionator, piper):
    options = {"n"}
    print()
    if piper:
        print(f"Perform action '{piper.script}' (y)?")
        options.add("y")
    elif actionator.action_type == "markdone":
        print(f"Perform action 'markdone' (y)?")
        options.add("y")
    print("Advance to next item (n)?")
    if task.sub_tasks:
        print("There are subtasks - examine (e)?")
        options.add("e")

    answer = None
    while answer not in options:
        answer = input(" > ")
        answer = answer.lower()
        if answer not in options:
            print("Invalid choice!")
    return answer


def _non_interactive(tasks, actionator, piper, pipe_separately: bool):
    for i, t in enumerate(tasks):
        print("--")
        print(f"Task {i}")
        _print_single_task(t)
        actionator.take_action(t)

    if piper:
        if pipe_separately:
            # Pipe X times for X tasks.
            for t in tasks:
                content = _serialize_task(t)
                piper.pipe(content)
        else:
            # Pipe once for each task.
            content = [_serialize_task(t) for t in tasks]
            piper.pipe(content)
    print()


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


def _print_single_task(task, ignore_sub_tasks=False):
    """Includes any sub_tasks it has."""
    print("Title: ", task.title)
    print("Description: ", task.notes)
    print("Last Updated: ", task._dict["updated"])
    if task.sub_tasks and not ignore_sub_tasks:
        print("Sub Tasks:")
        indent = " " * 4
        for sub_task in task.sub_tasks:
            print(f"{indent}--")
            print(f"{indent}Title: ", sub_task.title)
            print(f"{indent}Description: ", sub_task.notes)
            print(f"{indent}Last Updated: ", sub_task._dict["updated"])


def _filter_tasks(tasks, match, strategy="default"):
    """Filter out tasks based on title and description for the given string.

    If a parent doesn't match, the subtasks are ignored.
    """
    def is_match(task, term):
        return term in task.title.lower() or (task.notes and term in task.notes.lower())

    def default(tasks):
        tasks = [t for t in tasks if is_match(t, match)]
        for t in tasks:
            t.sub_tasks = [t for t in t.sub_tasks if is_match(t, match)]
        return tasks

    def parent_match(tasks):
        """Just check the parents, don't filter children."""
        tasks = [t for t in tasks if is_match(t, match)]
        return tasks

    strategies = {
        "default": default,
        "parent-match": parent_match,
    }
    filterer = strategies.get(strategy)

    if not filterer:
        raise ValueError(
            f"Could not find matching matching strategy for provided value: {strategy}"
        )

    match = match.lower()
    tasks = filterer(tasks)

    return tasks


class Actionator:
    def __init__(self, action_type):
        self.action_type = action_type

    def take_action(self, task):
        if self.action_type == "none":
            return
        elif self.action_type == "markdone":
            print("\nMarking as done!\n")
            task.complete = True


class Piper:
    def __init__(self, script):
        self.script = script

    def pipe(self, content):
        print(f"Piping to {self.script}:")
        json_content = json.dumps(content)
        subprocess.run(self.script, input=json_content, encoding="utf-8")
