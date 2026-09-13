from contextlib import suppress
from pathlib import Path
from tasker.tasks.task import Task
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

@command_fixture
def config():
    tasks_path = helpers.find_tasks_dir()

    return TaskerConfig.parse_file(tasks_path / ".config.toml")

@command_fixture
def tasks(config: Fixture[TaskerConfig]):
    all_tasks = []
    tasks_path = helpers.find_tasks_dir()

    dirs = helpers.find_all_task_paths(tasks_path)

    for task in dirs:
        try:
            all_tasks.append(Task.parse_file(task / config.root_file_name, int(task.name), config))
        except BaseException as err:
            logging.error(err)

    return all_tasks
