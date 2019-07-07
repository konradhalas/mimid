import abc
from typing import Any

from mimid.exceptions import ValueNotCapturedException


class ValueMatcher(abc.ABC):
    @abc.abstractmethod
    def __call__(self, other: Any) -> bool:
        pass

    @staticmethod
    def from_maybe_value(value) -> "ValueMatcher":
        if not isinstance(value, ValueMatcher):
            value = eq(value)
        return value


class any(ValueMatcher):
    def __call__(self, _: Any) -> bool:
        return True


class eq(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other == self.value


class gt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other > self.value


class gte(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other >= self.value


class lt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other < self.value


class lte(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, other: Any) -> bool:
        return other <= self.value


EMPTY_VALUE = object()


class CaptureSlot:
    def __init__(self):
        self._value = EMPTY_VALUE

    @property
    def value(self):
        if self._value is EMPTY_VALUE:
            raise ValueNotCapturedException()
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class capture(ValueMatcher):
    def __init__(self, slot: CaptureSlot) -> None:
        self.slot = slot

    def __call__(self, other: Any) -> bool:
        self.slot.value = other
        return True
