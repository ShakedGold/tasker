from typing import Annotated, Literal

from pydantic import BaseModel, Field


class EnumProperty(BaseModel):
    type: Literal["enum"]
    values: list[str]
    default: str | None = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, str):
            raise TypeError(f"Enum validation failed! {value} is not a string")

        if value not in self.values:
            raise ValueError(f"Enum validation failed! {value} not in {self.values}")


class NumberProperty(BaseModel):
    type: Literal["number"]
    min: float | None = None
    max: float | None = None
    default: float | None = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Number validation failed! {value} is not a number")

        if self.max and float(value) > self.max:
            raise ValueError(f"Number validation failed! {value} > {self.max}")

        if self.min and float(value) < self.min:
            raise ValueError(f"Number validation failed! {value} < {self.max}")


class ArrayProperty(BaseModel):
    type: Literal["array"]
    default: list[object] | None = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, list):
            raise TypeError(f"Array validation failed! {value} is not a list")


Property = Annotated[
    EnumProperty | NumberProperty | ArrayProperty,
    Field(discriminator="type"),
]


class ParsedProperty(BaseModel):
    property_type: Property
    value: object
