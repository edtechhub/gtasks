# Gtasks

A command line application to integrate with Google Tasks and perform some common operatations.

## Usage

To see usage options run:
```
gtask -h
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
```
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
