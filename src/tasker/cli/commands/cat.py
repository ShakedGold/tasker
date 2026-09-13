from rich.markdown import Markdown
from rich.console import Console
import logging
from cyclopts import App

from tasker.tasks.task import Task
from tasker.cli.commands.pre import Fixture

cat_app = App()

@cat_app.default
def cat(ids: list[int], syntax: bool = True, *, tasks: Fixture[list[Task]]):
    for task_id in ids:
        filtered_tasks = list(filter(lambda task: task.task_id == task_id, tasks))

        if len(filtered_tasks) == 0:
            logging.debug(f"task({task_id}): not found")
            continue

        task = filtered_tasks[0]
        if syntax:
            console = Console()
            md = Markdown(str(task))

            if len(ids) > 1:
                console.rule()
                console.print(f"{task.path}:")
            console.print(md)
        else:
            print(task)
