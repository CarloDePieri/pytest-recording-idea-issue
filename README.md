Ok, so this was a weird one to debug...

Simply having the `pytest-recording` plugin enabled breaks [Intellij Idea](https://www.jetbrains.com/idea/) pytest
[failed test reports](https://www.jetbrains.com/help/idea/product-tests.html) in some specific test cases
([here is an example](https://github.com/CarloDePieri/pytest-recording-idea-issue/blob/main/tests/test_issue.py)): 

- a test cassette is being recorded via plain `vcrpy` syntax or via `pytest-recording` decorator;
- two (or more) network calls are being executed and recorded: the first one succeeds, the second fails and then an
error is raised by `requests`' `raise_for_status()` method.

Instead of reporting the correct stack trace and main error, Idea reports there has been a failed string comparison
involving url paths.

My guess is that `pytest-recording` breaks something Idea's test runner relies on to generate errors messages, because:

- pytest output in the terminal is consistent and correct with or without the plugin installed;
- disabling the `pytest-recording` plugin in Idea ui by adding `-p no:recording` as additional argument restore the correct
  error message;
- removing the plugin also restore the correct error message.

### How to reproduce the issue

Checkout the minimal test repo with `git clone https://github.com/CarloDePieri/pytest-recording-idea-issue`.

Create a virtualenv and install all dependencies there:

```
cd pytest-recording-idea-issue
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

IMPORTANT: 

- this DOES NOT install `pytest-recording`;
- the test we are going to launch DOES NOT use this plugin decorator, but plain `vcrpy`.

Then:

- import the folder into Idea as a new project;
- add the created virtualenv as a python sdk for the project;
- run the test from the Idea ui: observe that the test fails with the **correct** error message reporting a 404;
- manually install `pytest-recording` with `pip install pytest-recording` in the venv;
- relaunch the test from the Idea ui: the error message is now **completely off track**: it reports a difference between
expected and actual values `'/api/users/23' != '/api/users/2'`.

#### Under the hood

Idea uses [this test runner](https://github.com/JetBrains/intellij-community/blob/09da58dedb5b39278df01c5dee01af19752d063d/python/helpers/pycharm/_jb_pytest_runner.py)
to launch pytest tests and generate the report message. Launching the script directly in the terminal shows indeed the
wrong error message when `pytest-recording` is installed.

#### Installed software versions

```
python: 3.10.4
pytest: 7.1.2
pytest-recording: 0.12.0
vcrpy: 4.1.1
requests: 2.27.1
Idea Ultimate: Build #IU-221.5591.52, built on May 10, 2022
os: arch linux
```
