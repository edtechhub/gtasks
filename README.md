# Gtasks

A command line application to integrate with Google Tasks and perform some common operatations.

## Usage

To see usage options run:
```
$ gtask -h

usage: gtasks [-h] {authenticate,backup,process} ...

positional arguments:
  {authenticate,backup,process}
    authenticate        Authenticate the use of your google account for access
                        to the google task APIs
    backup              Backup your tasks to a local JSON file
    process             Search Tasks and perform actions on them

optional arguments:
  -h, --help            show this help message and exit
```

Further documentation on usage TBD.

### Installing from Source

To install and run from source:

Requires and been tested on Python 3+.

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
