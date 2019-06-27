import abc
from typing import Any


class Matcher(abc.ABC):
    @abc.abstractmethod
    def __call__(self, other: Any) -> bool:
        pass


class gt(Matcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other > self.value


class lt(Matcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other < self.value
