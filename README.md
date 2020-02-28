
I was following this article for seting up env and develop:
https://towardsdatascience.com/how-to-setup-an-awesome-python-environment-for-data-science-or-anything-else-35d358cc95d5

And this one as How-to for CLI coding:
https://towardsdatascience.com/how-to-write-python-command-line-interfaces-like-a-pro-f782450caf0d
## **Pre-conditions**
Setup python 3.7+
Setup venv, you can use this: https://docs.python-guide.org/dev/virtualenvs/
## Setup
 1. git clone code of this tool to a directory you use for saving
    projects
 2. Install poetry through pip. You will find poetry in
    ~/.poetry/bin and can add it to your .bashrc as export
    PATH=$HOME/.poetry/bin:$PATH
pip install poetry
Use next  command below -> with this, the virutal environemnts created by poetry are located within the project. Helpful for ides like pycharm
```poetry config settings.virtualenvs.in-project true```
 4. Change to the directory where you cloned this project into
```cd cli_for_tdclient # The folder that you've clone the repo into```
 5. Install all dependencies. This might take a time as it creates the virutal environments
 ```poetry install ```
## In the pycharm:
Go to Preferences | Project: cli_for_tdclient | Project Interpreter and choose virtual env which was set up by poetry for you.
## Usage:

Activate virtual env ```source .venv/bin/activate```
 Now from terminal you can work with cli using python:

* python3 cli_for_tdclient/cli_for_tdclient.py -d nina -t test --limit 1 -e "presto"
Result: tdclient.errors.NotFoundError: Table 'nina.test' does not exist
* python3 cli_for_tdclient/cli_for_tdclient.py -d nina -t club --limit 1 -e "presto"
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d nina -t club
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d nina -t club -f csv
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -f csv -limit 2
Result: Error: no such option: -l
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -f csv --limit 2
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -c "*" -f csv --limit 2
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -c "test" -f csv --limit 2
Exception: Check your column param send correct name for column. This is correct list
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -c "status, id" -m 1582335915 -M 1582772285 -f csv --limit 2
Result: Query issued. File created/updated
* python3 cli_for_tdclient/cli_for_tdclient.py -d orders  -t orders -c "status, id" -m 1582335915 -M 1582772285 -f tab --limit 2
