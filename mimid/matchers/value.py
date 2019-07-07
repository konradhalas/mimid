import abc
from typing import Any


class ValueMatcher(abc.ABC):
    @abc.abstractmethod
    def __call__(self, other: Any) -> bool:
        pass


class gt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return self.value < other


class lt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return self.value > other


class eq(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return self.value == other
