import os
from pathlib import Path
import shutil
import logging
from cyclopts import App

import tasker.cli.helpers as helpers

rm_app = App()

@rm_app.default
def rm(ids: list[int]):
    """Delete tasks

    Parameters
    ----------
    ids:
        A list of task ids to remove
    """

    tasks_dir = helpers.find_tasks_dir()

    for task_path in tasks_dir.iterdir():
        if not task_path.is_dir():
            continue
        if not task_path.name.isdigit():
            continue

        if int(task_path.name) in ids:
            shutil.rmtree(task_path)
            print(f"Deleted task #{task_path.name} in {os.path.relpath(tasks_dir, Path.cwd())}/")
