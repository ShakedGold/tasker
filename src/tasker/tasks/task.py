from pathlib import Path
from pydantic import BaseModel
from typing import Final, TextIO
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

from tasker.config.property import Property, ParsedProperty
from tasker.config.config import TaskerConfig

"""
FORMAT OF TASK FILE:
---
<PROPERTY>: <VALUE>
---

# <TITLE>

<BODY>
"""

yaml = YAML()

class Task(BaseModel):
    properties: dict[str, ParsedProperty]
    title: str
    body: str

    @classmethod
    def _read_properties_section(cls, task_file: TextIO) -> str:
        if task_file.readline() == "---":
            raise SyntaxError("Expected '---' at the start of the file")

        properties = ""
        current_property_line = task_file.readline().strip()

        while current_property_line != "---":
            properties += current_property_line + "\n"
            current_property_line = task_file.readline().strip()

        return properties

    @classmethod
    def _parse_property(cls, property_name: str, property_content: object, config: TaskerConfig) -> ParsedProperty:
        tasker_property = config.properties.get(property_name)
        if tasker_property is None:
            raise ValueError(f"Invalid property detected! ({property_name}), available properties: {config.properties.keys()}")

        try:
            tasker_property.check(property_content)
        except ValueError as err:
            raise ValueError(f"Validation failed for: {property_name}! {err}") from err

        return ParsedProperty(property_type=tasker_property, value=property_content)

    @classmethod
    def _parse_properties_section(cls, task_file: TextIO, config: TaskerConfig):
        properties_section = cls._read_properties_section(task_file)

        try:
            properties_yaml: dict[str, object] = yaml.load(properties_section)
        except DuplicateKeyError as err:
            raise ValueError(f"Duplicated property! {err.problem}")

        properties: dict[str, object] = {}
        for property_name, property_content in properties_yaml.items():
            properties[property_name] = cls._parse_property(property_name, property_content, config)

        return properties

    @classmethod
    def _parse_title(cls, task_file: TextIO) -> str:
        empty_line = task_file.readline()

        if empty_line != "\n":
            raise ValueError(f"Expected empty seperating line between properties and title, found: {empty_line}")

        title_line = task_file.readline().strip()

        if not title_line.startswith("# "):
            raise ValueError(f"Expected title to be a markdown (h1) header! found: {title_line}")

        return title_line.removeprefix("# ")

    @classmethod
    def _parse_body(cls, task_file: TextIO) -> str:
        empty_line = task_file.readline()
        if empty_line != "\n":
            raise ValueError(f"Expected empty seperating line between title and body, found: {empty_line}")

        return task_file.read()

    @classmethod
    def parse_file(cls, path: str | Path, config: TaskerConfig):
        properties: str = ""

        with open(path, "r") as task_file:
            properties = cls._parse_properties_section(task_file, config)
            title = cls._parse_title(task_file)
            body = cls._parse_body(task_file)

        return cls(properties=properties, title=title, body=body)

