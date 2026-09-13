import os
import logging
import inspect

from cyclopts import App, Parameter
from typing import Annotated

from tasker.tasks.task import Task
from tasker.config.config import TaskerConfig
from tasker.cli.commands.pre import parse_fixtures
from tasker.cli.commands.app import app
from tasker.cli.commands.pre import FIXTURES
from tasker.cli.logs import setup_logging
from tasker.cli.commands.ls import ls_app
from tasker.cli.commands.edit import edit_app
from tasker.cli.commands.new import new_app
from tasker.cli.commands.cat import cat_app
from tasker.cli.commands.init import init_app
from tasker.cli.commands.find import find_app
from tasker.cli.commands.rm import rm_app

app.command(ls_app, name="ls")
app.command(edit_app, name="edit")
app.command(new_app, name="new")
app.command(rm_app, name="rm")
app.command(find_app, name="find")
app.command(init_app, name="init")
app.command(cat_app, name="cat")

@app.meta.default
def pre_command(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    verbose: Annotated[
        int,
        Parameter(
            name=["-v", "--verbose"],
            count=True,
            help="Increase verbosity (-v for INFO, -vv for DEBUG).",
        ),
    ] = 0,
):
    log_level = (logging.FATAL - (verbose * 10))
    setup_logging(log_level)

    command, bound, _ = app.parse_args(tokens)

    extra_kwargs = parse_fixtures(command)
    return command(*bound.args, **bound.kwargs, **extra_kwargs)

def main():
    try:
        app.meta()
    except SystemExit:
        return
    except BaseException as err:
        logging.fatal(str(err))

        if logging.getLogger().level != logging.FATAL:
            raise err

if __name__ == "__main__":
    main()
