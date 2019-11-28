# Gtasks

A command line application to integrate with Google Tasks and perform some common operatations.

## Usage

To see usage options run:
```
$ gtasks -h

usage: gtasks [-h] {authenticate,backup,process,quickadd,lists} ...

positional arguments:
  {authenticate,backup,process,quickadd,lists}
    authenticate        Authenticate the use of your google account for access
                        to the google task APIs
    backup              Backup your tasks to a local JSON file
    process             Search Tasks and perform actions on them
    quickadd            Quickly add a task to a given list
    lists               Display all of your Google Tasks Lists.

optional arguments:
  -h, --help            show this help message and exit
```

Authenticate your app:
```
$ gtasks authenticate
```

Backup tasks:
```
$ gtasks backup
Backing up!
Including hidden tasks
Adding list to backup: My Tasks
Adding list to backup: Another List
Creating backup in file: backup-2019-11-28T22:22:22.181719.json
```
or only include visible tasks in your backup:
```
$ gtasks backup --include visible
```

Quickly add a task:
```
$ gtasks quickadd --list "My Tasks" "Buy some milk"
```

Process through your tasks, it has quite a few options, so see the help for more info:
```
$ gtasks process -h
```

### Installing from Source

To install and run from source:

Requires and been tested on Python 3+.

Check what version of python you are running.
```
python --version
```
If you're system python is Python 2 you will have to use `pip3` in the below steps instead of `pip`.

Clone the repository:

```
git clone git@github.com:edtechhub/gtasks.git
```
Install the dependencies (preferably in a virtual environment):

We require a two stage install, as the Gtasks installer itself requires some dependencies.
```
pip install -r pre-requirements.txt
pip install -r requirements.txt
```

For convenience you may symlink the `gtasks` executable to somewhere on your path, so that you can run `gtasks`.

### Installing via PyPi

TBD

## Running the tests

There is only one test file right now. To run:
```
python -m unittest tasks/tests/test_backup.py
```
If more tests are neccesary in future may expand into a full test runner, using pytest/nose or similar.
