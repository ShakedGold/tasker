import os
import shutil
from pathlib import Path

from cyclopts import App

from tasker.cli import helpers

rm_app = App()


@rm_app.default
def rm(ids: list[str]):
    """Delete tasks

    Parameters
    ----------
    ids:
        A list of task ids to remove
    """

    tasks_dir = helpers.find_tasks_dir()

    for task_id in ids:
        task_path = helpers.find_single_task_by_partial_id(task_id, tasks_dir)

        shutil.rmtree(task_path)
        print(f"Deleted task '{task_path.name}' in {os.path.relpath(tasks_dir, Path.cwd())}/")
