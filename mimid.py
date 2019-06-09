from collections import defaultdict
from typing import Type, TypeVar, Dict, Optional, cast, NamedTuple

T = TypeVar("T")


class Mock:
    def __init__(self, cls: Type) -> None:
        self.cls = cls
        self.mock_attrs: Dict[str, MockAttribute] = {}

    def __getattr__(self, attr):
        if attr not in self.mock_attrs:
            self.mock_attrs[attr] = MockAttribute(self, attr)
        return self.mock_attrs[attr]


class MockAttribute:
    def __init__(self, target: Mock, name: str) -> None:
        self.name = name
        self.target = target
        self.call_configurator = None
        self.calls: Dict[Call, int] = defaultdict(int)

    def __call__(self, *args, **kwargs):
        call = Call(args=args, kwargs=tuple(kwargs.items()))
        if self.call_configurator is not None and (
            self.call_configurator.call is None or self.call_configurator.call == call
        ):
            self.calls[call] += 1
            return self.call_configurator.return_value
        raise CallNotConfiguredException()


class Call(NamedTuple):
    args: tuple
    kwargs: tuple


class CallConfigurator:
    def __init__(self, mock_attr: MockAttribute) -> None:
        self.mock_attribute = mock_attr
        self.call: Optional[Call] = None
        self.return_value = None

    def with_args(self, *args, **kwargs) -> "CallConfigurator":
        self.call = Call(args=args, kwargs=tuple(kwargs.items()))
        return self

    def returns(self, value):
        self.return_value = value
        self.mock_attribute.call_configurator = self


class CallVerifier:
    def __init__(self, mock_attr: MockAttribute) -> None:
        self.mock_attr = mock_attr
        self.call: Optional[Call] = None

    def called_once(self):
        if (self.call and self.mock_attr.calls[self.call] != 1) or (
            not self.call and sum(self.mock_attr.calls.values()) == 0
        ):
            raise NotCalledException()

    def with_args(self, *args, **kwargs) -> "CallVerifier":
        self.call = Call(args=args, kwargs=tuple(kwargs.items()))
        return self


def mock(cls: Type[T]) -> T:
    return cast(T, Mock(cls))


def every(mock_attr: MockAttribute) -> CallConfigurator:
    return CallConfigurator(mock_attr)


def verify(mock_attr: MockAttribute) -> CallVerifier:
    return CallVerifier(mock_attr=mock_attr)


class MimidException(Exception):
    pass


class CallNotConfiguredException(MimidException):
    pass


class NotCalledException(MimidException):
    pass
