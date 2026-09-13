import os
import logging
import enum
from pathlib import Path
from typing import Annotated, Optional
from cyclopts import Parameter, App

from tasker.config.config import TaskerConfig
from tasker.tasks.task import Task
from tasker.cli.commands.pre import Fixture
from tasker.cli.commands.app import app

ls_app = App(help="List all tasks")

class Format(enum.StrEnum):
    FILES = "files"
    TITLE = "title"
    PROPS = "props"

@ls_app.default
def ls(
        format: Annotated[Optional[list[Format]], Parameter(alias="-f", consume_multiple=True, allow_repeating=False)] = None,
        properties: Annotated[Optional[list[str]], Parameter(alias="-p", consume_multiple=True, allow_repeating=True)] = None,
        *,
        config: Fixture[TaskerConfig],
        tasks: Fixture[list[Task]]
):
    """List the tasks in tasker

    Parameters
    ----------
    format:
        How to format the output (what to show/hide)
    properties:
        What properties to show
    """

    if format is None:
        format = [Format.FILES, Format.TITLE, Format.PROPS]

    if len(format) == 0:
        logging.error("Format list length cannot be 0")
        return

    if properties is None:
        properties = []

    for property_to_show in properties:
        if property_to_show not in config.properties.keys():
            logging.error(f'property "{property_to_show}" does not exist')
            return

    for task in tasks:
        task_line = []

        if Format.FILES in format:
            task_line.append(os.path.relpath(task.path, Path.cwd()))

        if Format.TITLE in format:
            task_line.append(task.title)

        if Format.PROPS in format:
            properties_line = []
            for property_to_show in properties:
                if property_to_show not in task.properties.keys():
                    continue
                
                properties_line.append(f"{property_to_show}={task.properties[property_to_show].value}")

            if len(properties_line) > 0:
                task_line.append(",".join(properties_line))

        print("|".join(task_line))

