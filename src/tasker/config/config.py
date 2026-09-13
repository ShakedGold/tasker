import tomllib

from typing import Self, TYPE_CHECKING
from pathlib import Path
from tasker.config.property import Property
from pydantic import BaseModel
from pydantic.deprecated.parse import Protocol as DeprecatedParseProtocol


class TaskerConfig(BaseModel):
    root_file_name: str = "README.md"
    properties: dict[str, Property]

    @classmethod
    def parse_file(
        cls,
        path: str | Path,
        *,
        content_type: str | None = None,
        encoding: str = 'utf8',
        proto: DeprecatedParseProtocol | None = None,
        allow_pickle: bool = False,
    ) -> Self:
        is_toml = (isinstance(path, str) and path.endswith(".toml") or (isinstance(path, Path) and path.suffix == ".toml") or (content_type == "toml"))

        if not is_toml:
            return super().parse_file(path, content_type=content_type, encoding=encoding, proto=proto, allow_pickle=allow_pickle)

        with open(path, "rb") as config_file:
            config_data = tomllib.load(config_file)

        return cls.model_validate(config_data)
