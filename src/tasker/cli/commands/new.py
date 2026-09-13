from tasker.tasks.task import Task
from tasker.config.config import TaskerConfig
from tasker.cli.commands.pre import Fixture
import os
from tasker.cli.commands.edit import edit, edit_task
from pathlib import Path
import logging
from cyclopts import App

import tasker.cli.helpers as helpers

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

    new_task_id = len(helpers.find_all_task_paths(tasks_dir)) + 1
    task = Task.create_default(new_task_id, config)

    if edit:
        edit_task(task.path)
    else:
        print(f"Created task #{new_task_id} in {os.path.relpath(tasks_dir, Path.cwd())}/")
