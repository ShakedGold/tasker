import logging
from pathlib import Path
from cyclopts import App

import tasker.cli.helpers as helpers

DEFAULT_CONFIG = """\
[properties.status]
type = "enum"
values = ["open", "closed"]

[properties.priority]
type = "number"
min = 0
max = 100

[properties.kind]
type = "enum"
values = ["bug", "feature", "test"]

[properties.tags]
type = "array"
"""

init_app = App()

@init_app.default
def init():
    tasker_dir = Path.cwd() / helpers.TASKER_DIR_NAME

    if tasker_dir.exists():
        raise RuntimeError(f"{helpers.TASKER_DIR_NAME} already exists!")

    tasker_dir.mkdir()

    (tasker_dir / ".config.toml").write_text(DEFAULT_CONFIG)
    logging.info(f"Created a tasker project in {Path.cwd()}")
