from pathlib import Path
import logging
from tasker.tasks.task import Task
from tasker.cli.commands.pre import Fixture
import os
from cyclopts import App

edit_app = App()

def edit_task(task_path: Path):
    editor = os.environ.get("EDITOR") or "vi"
    os.execlp(editor, editor, task_path)

@edit_app.default
def edit(id: int, *, tasks: Fixture[list[Task]]):
    """Open $EDITOR on the task [id]/README.md

    Parameters
    ----------
    id:
        The task id to edit
    """

    filtered_tasks = list(filter(lambda task: task.task_id == id, tasks))

    if len(filtered_tasks) == 0:
        raise RuntimeError(f"task({id}) not found")

    edit_task(filtered_tasks[0].path)
