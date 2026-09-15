import json
from tasker.config.config import TaskerConfig
import logging
from pathlib import Path

from cyclopts import App

from tasker.cli import helpers

DEFAULT_CONFIG = """\
#:schema ./.config.schema.json

root_file_name = "README.md"

[generation]
method = "counter"

[properties.status]
type = "enum"
values = ["open", "closed"]
default = "open"

[properties.priority]
type = "number"
min = 0
max = 100
default = 999

[properties.kind]
type = "enum"
values = ["bug", "feature", "test"]
default = "FILL-ME"

[properties.tags]
type = "array"
"""

init_app = App()


@init_app.default
def init():
    """
    Initialize a tasker project (creates .tasker and .tasker/.config.toml)
    """

    tasker_dir = Path.cwd() / helpers.TASKER_DIR_NAME

    if tasker_dir.exists():
        raise RuntimeError(f"{helpers.TASKER_DIR_NAME} already exists!")

    tasker_dir.mkdir()

    schema_path = tasker_dir / ".config.schema.json"
    schema_path.write_text(json.dumps(TaskerConfig.model_json_schema()))

    logging.debug(f"created {schema_path}")

    tasker_config = tasker_dir / ".config.toml"
    tasker_config.write_text(DEFAULT_CONFIG)

    logging.debug(f"created {tasker_config}")
    logging.info(f"Created a tasker project in {Path.cwd()}")
