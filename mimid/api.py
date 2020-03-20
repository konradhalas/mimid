from typing import Union, Any, Type, TypeVar, cast

from mimid.configuration import (
    MockCallable,
    Mock,
    MockCallableConfigurator,
    MockPropertyConfigurator,
    MockEffectsConfigurator,
    MockArgsConfigurator,
    MockPropertyGetter,
    MockProperty,
)
from mimid.matchers.value import CaptureSlot
from mimid.verification import MockAttributeVerifier

T = TypeVar("T")


def mock(target: Type[T]) -> T:
    return cast(T, Mock(target))


def prop(target: T) -> T:
    return cast(T, MockPropertyGetter(cast(Mock, target)))


def every(target: Union[MockCallable, MockProperty, Mock, Any]) -> Union[MockEffectsConfigurator, MockArgsConfigurator]:
    if isinstance(target, MockCallable):
        return MockCallableConfigurator(target)
    elif isinstance(target, MockProperty):
        return MockPropertyConfigurator(target)
    elif isinstance(target, Mock):
        return MockCallableConfigurator(target.mock_callable)
    raise TypeError()


def verify(target: Union[MockCallable, Mock, Any]) -> MockAttributeVerifier:
    if isinstance(target, MockCallable):
        return MockAttributeVerifier(target)
    elif isinstance(target, Mock):
        return MockAttributeVerifier(target.mock_callable)
    raise TypeError()


def slot() -> CaptureSlot:
    return CaptureSlot()
