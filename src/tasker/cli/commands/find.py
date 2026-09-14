from abc import ABC
from enum import IntEnum, StrEnum

from cyclopts import App

from tasker.cli.commands.pre import Fixture
from tasker.config.config import TaskerConfig
from tasker.tasks.task import Task

find_app = App()


class OperationState(IntEnum):
    PROPERTY = (0,)
    OP = (1,)
    VALUE = (2,)
    LOGICAL = (3,)


class LogicalOperations(StrEnum):
    AND = "and"
    OR = "or"


class Operations(StrEnum):
    HAS = "has"
    EQ = "eq"
    NEQ = "neq"
    GTE = "gte"
    GT = "gt"
    LT = "lt"
    LTE = "lte"


class Operation(ABC):
    def exec(self) -> bool:
        raise NotImplementedError


class BinaryOperation(Operation):
    def __init__(self, a: object | None, b: object | None, op: Operations | LogicalOperations):
        self.a = a
        self.b = b
        self.op = op

    def _is_number(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def exec(self) -> bool:
        if self.a is None or self.b is None:
            return False

        if self.op in [Operations.GT, Operations.GTE, Operations.LT, Operations.LTE]:
            if not self._is_number(str(self.a)):
                raise TypeError(f"TQL Failure: {self.a} is not a number")
            if not self._is_number(str(self.b)):
                raise TypeError(f"TQL Failure: {self.b} is not a number")

        if self.op == Operations.HAS:
            return self.b in self.a
        elif self.op == Operations.EQ:
            return str(self.a) == str(self.b)
        elif self.op == Operations.NEQ:
            return str(self.a) != str(self.b)
        elif self.op == Operations.GTE:
            return float(self.a) >= float(self.b)
        elif self.op == Operations.GT:
            return float(self.a) > float(self.b)
        elif self.op == Operations.LTE:
            return float(self.a) <= float(self.b)
        elif self.op == Operations.LT:
            return float(self.a) < float(self.b)
        elif self.op == LogicalOperations.AND:
            return self.a and self.b
        elif self.op == LogicalOperations.OR:
            return self.a or self.b


class OperationStateMachine:
    def __init__(self, config: TaskerConfig):
        self.state = OperationState.PROPERTY
        self.stack: list[tuple[OperationState, object]] = []
        self.config = config

    def _handle_property(self, value: str):
        if not value.startswith("."):
            raise ValueError(f"TQL Failure: expected '.' found {value}")

        property_value = value[1:]
        task_property = self.config.properties.get(property_value)
        if task_property is None:
            raise ValueError(f"TQL Failure: invalid property {property_value} does not exist")

        self.stack.append((self.state, property_value))
        self.state = OperationState.OP

    def _handle_operation(self, value: str):
        if value not in Operations.__members__.values():
            raise ValueError(
                f"TQL Failure: operation: '{value}' is not supported, supported operations: {[v.value for v in Operations.__members__.values()]}"
            )

        op = Operations(value)
        self.stack.append((self.state, op))
        self.state = OperationState.VALUE

    def _handle_value(self, value: str):
        self.stack.append((self.state, value))
        self.state = OperationState.LOGICAL

    def _handle_logical(self, value: str):
        if value not in LogicalOperations.__members__.values():
            raise ValueError(
                f"TQL Failure: logical operation: '{value}' is not supported, supported operations: {[v.value for v in LogicalOperations.__members__.values()]}"
            )

        op = LogicalOperations(value)
        self.stack.append((self.state, op))
        self.state = OperationState.PROPERTY

    def handle(self, value: str):
        if self.state == OperationState.PROPERTY:
            self._handle_property(value)
        elif self.state == OperationState.OP:
            self._handle_operation(value)
        elif self.state == OperationState.VALUE:
            self._handle_value(value)
        elif self.state == OperationState.LOGICAL:
            self._handle_logical(value)

    def _create_operation(self, stack: list[object]) -> Operation:
        if len(stack) == 3:  # Binary
            a, op, b = stack
            return BinaryOperation(a, b, op)
        else:
            raise ValueError(
                f"TQL Failure: unsupported operation ({len(stack)}) size operation is unsupported"
            )

    def _logical_operation(self, task_stack: list[object], value: object, amount: int):
        remaining = task_stack[len(task_stack) - amount :]
        operation = self._create_operation(remaining)

        for _ in range(amount):
            task_stack.pop()

        task_stack.append(operation.exec())

    def parse(self, task: Task) -> bool:
        task_stack = []
        amount_left = 0

        for state, value in self.stack:
            if state == OperationState.PROPERTY:
                task_property = task.properties.get(value)

                # could be null, signifying that it does not exist on the task
                if task_property is None:
                    task_stack.append(None)
                else:
                    task_stack.append(task_property.value)
                amount_left += 1
            elif state == OperationState.OP:
                task_stack.append(value.value)
                amount_left += 1
            elif state == OperationState.VALUE:
                task_stack.append(value)
                amount_left += 1
            elif state == OperationState.LOGICAL:
                if amount_left < 3:
                    continue

                self._logical_operation(task_stack, value, amount_left)
                task_stack.append(value)

                amount_left = 0

        self._logical_operation(task_stack, value, amount_left)

        result = []
        for op in task_stack:
            result.append(op)
            if len(result) == 3:
                a, op, b = result
                result.clear()
                result.append(BinaryOperation(a, b, op).exec())

        return result[0]


@find_app.default
def find(query: list[str], *, config: Fixture[TaskerConfig], tasks: Fixture[list[Task]]):
    """Find tasks based on the task query language (TQL)

    Parameters
    ----------
    query:
        The query you want to search for
    """

    state_machine = OperationStateMachine(config)

    for operation in query:
        state_machine.handle(operation)

    for task in tasks:
        result = state_machine.parse(task)
        if result:
            print(repr(task))
