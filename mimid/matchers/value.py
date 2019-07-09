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

    def __or__(self, other: "ValueMatcher") -> "ValueMatcher":
        return OrValueMatcher(self, other)

    def __and__(self, other: "ValueMatcher") -> "ValueMatcher":
        return AndValueMatcher(self, other)

    def __invert__(self) -> "ValueMatcher":
        return NotValueMatcher(self)


class OrValueMatcher(ValueMatcher):
    def __init__(self, first: ValueMatcher, second: ValueMatcher) -> None:
        self.first = first
        self.second = second

    def __call__(self, value: Any) -> bool:
        return self.first(value) or self.second(value)


class AndValueMatcher(ValueMatcher):
    def __init__(self, first: ValueMatcher, second: ValueMatcher) -> None:
        self.first = first
        self.second = second

    def __call__(self, value: Any) -> bool:
        return self.first(value) and self.second(value)


class NotValueMatcher(ValueMatcher):
    def __init__(self, matcher: ValueMatcher) -> None:
        self.matcher = matcher

    def __call__(self, value: Any) -> bool:
        return not self.matcher(value)


class any(ValueMatcher):
    def __call__(self, _: Any) -> bool:
        return True


class eq(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any) -> bool:
        return value == self.value


class gt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any) -> bool:
        return value > self.value


class gte(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any) -> bool:
        return value >= self.value


class lt(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any) -> bool:
        return value < self.value


class lte(ValueMatcher):
    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any) -> bool:
        return value <= self.value


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

    def __call__(self, value: Any) -> bool:
        self.slot.value = value
        return True
