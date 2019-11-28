"""In charge of kicking off a request from the user for authentication to their Google Tasks."""
from gtasks import Gtasks


def authenticate():
    """Simply construct a Gtasks object which will prompt authentication."""
    Gtasks()
