from tasker.config.config import TaskerConfig
import os
import logging

from pathlib import Path
from cyclopts import App

from tasker.tasks.task import Task
from tasker.cli.commands.pre import Fixture
import tasker.cli.helpers as helpers

edit_app = App()

def edit_task(task_path: Path):
    editor = os.environ.get("EDITOR") or "vi"
    os.execlp(editor, editor, task_path)

@edit_app.default
def edit(task_id: str, *, config: Fixture[TaskerConfig]):
    """Open $EDITOR on the task [id]/[root_file_name]

    Parameters
    ----------
    task_id:
        The task id to edit
    """

    
    task_dir = helpers.find_tasks_dir()
    task = helpers.find_single_task_by_partial_id(task_id, task_dir)
    edit_task(task / config.root_file_name)
