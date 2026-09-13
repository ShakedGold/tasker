from pathlib import Path
from asyncio import all_tasks
from tasker.tasks.task import Task
from markdown_it.cli.parse import parse_args
import functools
import os
import logging
import inspect

from tasker.config.config import TaskerConfig
from cyclopts import Parameter
from typing import Callable, Annotated, Generic, TypeVar, get_origin, get_type_hints, get_args

from tasker.cli.commands.app import app
import tasker.cli.helpers as helpers

T = TypeVar("T")

class FixtureParam(Generic[T]):
    pass

Fixture = Annotated[T, FixtureParam[T], Parameter(parse=False)]

FIXTURES: dict[str, Callable] = {}

def command_fixture(fixture):
    FIXTURES[fixture.__name__] = fixture
    return fixture

def get_fixture_type(annotation):
    if get_origin(annotation) is Annotated:
        return get_args(annotation)[1]
    return annotation

def parse_fixtures(command):
    results = {}
    annotations = get_type_hints(command, include_extras=True)

    for arg, annotation in annotations.items():
        base_type = get_origin(get_fixture_type(annotation))

        if base_type is not FixtureParam:
            continue

        fixture = FIXTURES.get(arg)
        fixture_params = parse_fixtures(fixture)

        if fixture is not None:
            results[arg] = fixture(**fixture_params)

    return results

@app.meta.default
def pre_command(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
):
    command, bound, _ = app.parse_args(tokens)

    extra_kwargs = parse_fixtures(command)
    return command(*bound.args, **bound.kwargs, **extra_kwargs)

@command_fixture
def config():
    tasks_path = helpers.find_tasks_dir()

    if tasks_path is None:
        raise RuntimeError("Not in a tasker project")

    return TaskerConfig.parse_file(tasks_path / ".config.toml")

@command_fixture
def tasks(config: Fixture[TaskerConfig]):
    all_tasks = []
    tasks_path = helpers.find_tasks_dir()

    if tasks_path is None:
        raise RuntimeError("Not in a tasker project")

    dirs = helpers.find_all_task_paths(tasks_path)

    for task in dirs:
        all_tasks.append(Task.parse_file(task / "README.md", int(task.name), config))

    return all_tasks
