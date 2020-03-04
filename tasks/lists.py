from gtasks import Gtasks


def lists():
    g = Gtasks()
    lists_ = g.get_lists()
    names = [l.title for l in lists_]
    print("Found Lists:")
    print("\n".join(names))
