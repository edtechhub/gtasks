from .process import _find_list_with_name


def quick_add(target_list, title):
    list_ = _find_list_with_name(target_list)
    if list_ is None:
        return

    list_.new_task(title=title)
    print(f"Task added successfully!")
