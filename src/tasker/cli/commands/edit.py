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
def edit(id: int, *, config: Fixture[TaskerConfig]):
    """Open $EDITOR on the task [id]/[root_file_name]

    Parameters
    ----------
    id:
        The task id to edit
    """

    
    task_dir = helpers.find_tasks_dir()
    tasks = helpers.find_all_task_paths(task_dir)

    filtered_tasks = list(filter(lambda task: int(task.name) == id, tasks))

    if len(filtered_tasks) == 0:
        raise RuntimeError(f"task({id}) not found")

    edit_task(filtered_tasks[0] / config.root_file_name)
