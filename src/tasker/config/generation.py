import random
import secrets
from enum import StrEnum
from typing import Never

from pydantic import BaseModel, Field

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
ZBASE32_LETTERS = "ybndrfg8ejkmcpqxot1uwisza345h769"
CROCKFORD_LETTERS = "0123456789abcdefghjkmnpqrstvwxyz"


class GenerationParams(BaseModel):
    separator: str = Field(default="-")
    "The ID section separation to use"

    letter_count: int = Field(default=5)
    "The amount of letters used in each section (ignored in counter)"

    section_count: int = Field(default=2)
    "The amount of sections used ID (ignored in counter)"


def assert_never(arg: Never) -> Never:
    raise AssertionError("Expected code to be unreachable")


def counter(tasks_ids):
    biggest_id = int(max(tasks_ids or [0], key=int))
    return str(biggest_id + 1)


def generate_id(letters: list[str], params: GenerationParams):
    result = [
        "".join(random.choices(letters, k=params.letter_count)) for _ in range(params.section_count)
    ]

    return params.separator.join(result)


def proquint(params: GenerationParams):
    sections = []
    for _ in range(params.section_count):
        section = "".join(
            [
                secrets.choice(CONSONANTS if position % 2 == 0 else VOWELS)
                for position in range(params.letter_count)
            ]
        )
        sections.append(section)

    return params.separator.join(sections)


class GenerationMethod(StrEnum):
    COUNTER = ("counter",)  # 1, 2, ...
    ZBASE32 = (
        "z-base-32",
    )  # https://en.wikipedia.org/wiki/Base32#cite_note-10:~:text=z%2Dbase%2D32edit
    CROCKFORD = (
        "crockford",
    )  # https://en.wikipedia.org/wiki/Base32#cite_note-10:~:text=Crockford%27s%20Base32edit
    PROQUINT = ("proquint",)  # https://arxiv.org/html/0901.4016

    def generate(self, params: GenerationParams, tasks_ids: list[str]) -> str:
        match self.value:
            case self.COUNTER:
                return counter([task_path.name for task_path in tasks_ids])
            case self.ZBASE32:
                return generate_id(ZBASE32_LETTERS, params)
            case self.CROCKFORD:
                return generate_id(CROCKFORD_LETTERS, params)
            case self.PROQUINT:
                return proquint(params)
            case _:
                assert_never(self.value)


class TaskerGenerationConfig(BaseModel):
    method: GenerationMethod = Field(default=GenerationMethod.COUNTER)
    "What method tasker use to generate the task IDs"

    parameters: GenerationParams = Field(default=GenerationParams())
    "The parameters of the task generation"
