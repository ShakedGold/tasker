import logging
from typing import Annotated

from cyclopts import Parameter

from tasker.cli.commands.app import app
from tasker.cli.commands.cat import cat_app
from tasker.cli.commands.edit import edit_app
from tasker.cli.commands.find import find_app
from tasker.cli.commands.init import init_app
from tasker.cli.commands.ls import ls_app
from tasker.cli.commands.new import new_app
from tasker.cli.commands.pre import parse_fixtures
from tasker.cli.commands.rm import rm_app
from tasker.cli.logs import setup_logging

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
        bool,
        Parameter(
            name=["-v", "--verbose"],
            help="Increase verbosity (-v for DEBUG).",
        ),
    ] = False,
):
    if verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    command, bound, _ = app.parse_args(tokens)

    extra_kwargs = parse_fixtures(command)
    return command(*bound.args, **bound.kwargs, **extra_kwargs)


def main():
    try:
        app.meta()
    except SystemExit:
        return
    except BaseException as err:
        error_message = str(err)
        if len(error_message) == 0:
            logging.fatal(repr(err))
        else:
            logging.fatal(error_message)

        if logging.getLogger().level != logging.INFO:
            raise
