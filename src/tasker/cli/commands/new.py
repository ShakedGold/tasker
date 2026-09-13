import os
from tasker.cli.commands.edit import edit, edit_task
from pathlib import Path
import logging
from cyclopts import App

import tasker.cli.helpers as helpers

new_app = App()

@new_app.default
def new(edit: bool = True):
    """Create a new task

    Parameters
    ----------
    edit:
        Open $EDITOR on the created task
    """

    tasks_dir = helpers.find_tasks_dir()

    if tasks_dir is None:
        logging.critical("Not in a tasker project")
        return

    new_task_id = len(helpers.find_all_task_paths(tasks_dir)) + 1
    new_task_path = Path(tasks_dir) / str(new_task_id)

    new_task_path.mkdir()

    readme_task = new_task_path / "README.md"

    with open(readme_task, "w+") as readme_file:
        readme_file.writelines([
            "---",
            "\n",
            "---",
            "\n",
            "\n",
            "# TASK TITLE",
        ])

    if edit:
        edit_task(readme_task)
    else:
        print(f"Created task #{new_task_id} in {os.path.relpath(tasks_dir, Path.cwd())}/")
