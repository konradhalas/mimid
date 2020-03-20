import abc
import functools
from typing import Optional, Any, List, Dict, Callable

from mimid.common import CallArguments
from mimid.exceptions import CallNotConfiguredException
from mimid.matchers.call import SpecificCallArgumentsMatcher, AnyCallArgumentsMatcher, CallArgumentsMatcher


class CallConfiguration:
    def __init__(
        self,
        call_arguments_matcher: CallArgumentsMatcher,
        return_values: Optional[List[Any]] = None,
        exception: Optional[Exception] = None,
        callable: Optional[Callable[[], Any]] = None,
    ) -> None:
        self.call_arguments_matcher = call_arguments_matcher
        self.exception = exception
        self.return_values = return_values
        self.callable = callable

    def match(self, call_arguments: CallArguments) -> bool:
        return self.call_arguments_matcher.match(call_arguments)

    def execute(self) -> Any:
        if self.exception is not None:
            raise self.exception
        if self.return_values is not None:
            if len(self.return_values) > 1:
                return self.return_values.pop(0)
            else:
                return self.return_values[0]
        if self.callable is not None:
            return self.callable()
        raise ValueError("Wrong configuration")


class MockCallable:
    def __init__(self, target) -> None:
        self.target = target
        self.call_configurations: List[CallConfiguration] = []
        self.calls_arguments: List[CallArguments] = []

    def __call__(self, *args, **kwargs) -> Any:
        call_arguments = CallArguments(args=args, kwargs=kwargs)
        call_arguments.bind(self.target)
        self.calls_arguments.append(call_arguments)
        for call_configuration in self.call_configurations:
            if call_configuration.match(call_arguments):
                return call_configuration.execute()
        raise CallNotConfiguredException()

    def add_configuration(self, call_configuration: CallConfiguration) -> None:
        self.call_configurations.append(call_configuration)


class Mock:
    def __init__(self, target: Any) -> None:
        self.target = target
        self.mock_attr_callable: Dict[str, MockCallable] = {}
        self.mock_callable = MockCallable(self.target)
        self.property_configurations: Dict[str, CallConfiguration] = {}

    def __getattr__(self, attr: str) -> MockCallable:
        if attr in self.property_configurations:
            return self.property_configurations[attr].execute()
        if attr not in self.mock_attr_callable:
            unbound_method = getattr(self.target, attr)
            bound_method = functools.partial(unbound_method, None)
            bound_method.__name__ = unbound_method.__name__  # type: ignore
            self.mock_attr_callable[attr] = MockCallable(bound_method)
        return self.mock_attr_callable[attr]

    def __call__(self, *args, **kwargs):
        return self.mock_callable(*args, **kwargs)

    def add_property_configuration(self, property_: str, call_configuration: CallConfiguration):
        self.property_configurations[property_] = call_configuration


class MockProperty:
    def __init__(self, mock: Mock, property_: str) -> None:
        self.mock = mock
        self.property = property_


class MockPropertyGetter:
    def __init__(self, mock: Mock) -> None:
        self.mock = mock

    def __getattr__(self, attr: str) -> MockProperty:
        if not hasattr(self.mock.target, attr):
            raise AttributeError(f"'{self.mock.target}' object has no attribute '{attr}'")
        return MockProperty(self.mock, attr)


class MockEffectsConfigurator(abc.ABC):
    @abc.abstractmethod
    def returns(self, value: Any) -> None:
        pass

    @abc.abstractmethod
    def raises(self, exception: Exception) -> None:
        pass

    @abc.abstractmethod
    def returns_many(self, values: List[Any]) -> None:
        pass

    @abc.abstractmethod
    def execute(self, callable: Callable[[], Any]):
        pass


class MockArgsConfigurator(abc.ABC):
    def with_args(self, *args, **kwargs) -> MockEffectsConfigurator:
        pass


class MockCallableConfigurator(MockArgsConfigurator, MockEffectsConfigurator):
    def __init__(self, mock_callable: MockCallable) -> None:
        self.mock_callable = mock_callable
        self.call_arguments_matcher: CallArgumentsMatcher = AnyCallArgumentsMatcher()

    def with_args(self, *args, **kwargs) -> "MockCallableConfigurator":
        self.call_arguments_matcher = SpecificCallArgumentsMatcher(
            target=self.mock_callable.target, arguments=CallArguments(args=args, kwargs=kwargs)
        )
        return self

    def returns(self, value: Any) -> None:
        self.mock_callable.add_configuration(
            CallConfiguration(call_arguments_matcher=self.call_arguments_matcher, return_values=[value])
        )

    def raises(self, exception: Exception) -> None:
        self.mock_callable.add_configuration(
            CallConfiguration(call_arguments_matcher=self.call_arguments_matcher, exception=exception)
        )

    def returns_many(self, values: List[Any]) -> None:
        self.mock_callable.add_configuration(
            CallConfiguration(call_arguments_matcher=self.call_arguments_matcher, return_values=values)
        )

    def execute(self, callable: Callable[[], Any]):
        self.mock_callable.add_configuration(
            CallConfiguration(call_arguments_matcher=self.call_arguments_matcher, callable=callable)
        )


class MockPropertyConfigurator(MockEffectsConfigurator):
    def __init__(self, mock_property: MockProperty) -> None:
        self.mock_property = mock_property

    def raises(self, exception: Exception) -> None:
        self.mock_property.mock.add_property_configuration(
            self.mock_property.property,
            CallConfiguration(call_arguments_matcher=AnyCallArgumentsMatcher(), exception=exception),
        )

    def returns(self, value: Any) -> None:
        self.mock_property.mock.add_property_configuration(
            self.mock_property.property,
            CallConfiguration(call_arguments_matcher=AnyCallArgumentsMatcher(), return_values=[value]),
        )

    def returns_many(self, values: List[Any]) -> None:
        self.mock_property.mock.add_property_configuration(
            self.mock_property.property,
            CallConfiguration(call_arguments_matcher=AnyCallArgumentsMatcher(), return_values=values),
        )

    def execute(self, callable: Callable[[], Any]):
        self.mock_property.mock.add_property_configuration(
            self.mock_property.property,
            CallConfiguration(call_arguments_matcher=AnyCallArgumentsMatcher(), callable=callable),
        )
