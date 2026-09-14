import os
from pathlib import Path

from cyclopts import App

from tasker.cli import helpers
from tasker.cli.commands.edit import edit_task
from tasker.cli.commands.pre import Fixture
from tasker.config.config import TaskerConfig
from tasker.tasks.task import Task

new_app = App()


@new_app.default
def new(edit: bool = True, *, config: Fixture[TaskerConfig]):
    """Create a new task

    Parameters
    ----------
    edit:
        Open $EDITOR on the created task
    """

    tasks_dir = helpers.find_tasks_dir()

    task = Task.create_default(config.generation.method, config)

    if edit:
        edit_task(task.path)
    else:
        print(f"Created task '{task.task_id}' in {os.path.relpath(tasks_dir, Path.cwd())}/")
