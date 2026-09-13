from tasker.cli.commands.init import init_app
from tasker.cli.commands.find import find_app
from tasker.cli.commands.rm import rm_app
import os
import logging
import inspect

from cyclopts import App, Parameter
from typing import Annotated

from tasker.tasks.task import Task
from tasker.config.config import TaskerConfig
from tasker.cli.commands.app import app
from tasker.cli.commands.pre import FIXTURES
from tasker.cli.logs import setup_logging
from tasker.cli.commands.ls import ls_app
from tasker.cli.commands.edit import edit_app
from tasker.cli.commands.new import new_app

app.command(ls_app, name="ls")
app.command(edit_app, name="edit")
app.command(new_app, name="new")
app.command(rm_app, name="rm")
app.command(find_app, name="find")
app.command(init_app, name="init")

def main():
    setup_logging()
    try:
        app.meta()
    except BaseException as err:
        logging.error(str(err))
