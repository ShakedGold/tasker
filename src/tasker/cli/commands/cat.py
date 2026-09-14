from rich.markdown import Markdown
from rich.console import Console
import logging
from cyclopts import App

from tasker.tasks.task import Task
from tasker.cli.commands.pre import Fixture
import tasker.cli.helpers as helpers

cat_app = App()

@cat_app.default
def cat(ids: list[str], syntax: bool = True, *, tasks: Fixture[list[Task]]):
    """Concat tasks and print them out

    Parameters
    ----------
    ids:
        The task ids to concat
    syntax:
        Display markdown formatting syntax highlighting
    """
    tasks_dir = helpers.find_tasks_dir()

    for task_id in ids:
        task = helpers.find_single_task_by_partial_id(task_id, tasks_dir)

        if syntax:
            console = Console()
            md = Markdown(str(task))

            if len(ids) > 1:
                console.rule()
                console.print(f"{task.path}:")
            console.print(md)
        else:
            print(task)
