from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field

class EnumProperty(BaseModel):
    type: Literal["enum"]
    values: list[str]
    default: Optional[str] = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, str):
            raise ValueError(f"Enum validation failed! {value} is not a string")

        if value not in self.values:
            raise ValueError(f"Enum validation failed! {value} not in {self.values}")


class NumberProperty(BaseModel):
    type: Literal["number"]
    min: float | None = None
    max: float | None = None
    default: Optional[float] = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Number validation failed! {value} is not a number")

        if self.max and float(value) > self.max:
            raise ValueError(f"Number validation failed! {value} > {self.max}")

        if self.min and float(value) < self.min:
            raise ValueError(f"Number validation failed! {value} < {self.max}")


class ArrayProperty(BaseModel):
    type: Literal["array"]
    default: Optional[list[object]] = Field(default=None)

    def check(self, value: object):
        if not isinstance(value, list):
            raise ValueError(f"Array validation failed! {value} is not a list")


Property = Annotated[
    EnumProperty | NumberProperty | ArrayProperty,
    Field(discriminator="type"),
]

class ParsedProperty(BaseModel):
    property_type: Property
    value: object

