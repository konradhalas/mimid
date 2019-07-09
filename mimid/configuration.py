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
    def __init__(self) -> None:
        self.call_configurations: List[CallConfiguration] = []
        self.calls_arguments: List[CallArguments] = []

    def __call__(self, *args, **kwargs) -> Any:
        call_arguments = CallArguments(args=args, kwargs=kwargs)
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
        self.mock_callable = MockCallable()

    def __getattr__(self, attr: str) -> MockCallable:
        if attr not in self.mock_attr_callable:
            self.mock_attr_callable[attr] = MockCallable()
        return self.mock_attr_callable[attr]

    def __call__(self, *args, **kwargs):
        return self.mock_callable(*args, **kwargs)


class MockCallableConfigurator:
    def __init__(self, mock_callable: MockCallable) -> None:
        self.mock_callable = mock_callable
        self.call_arguments_matcher: CallArgumentsMatcher = AnyCallArgumentsMatcher()

    def with_args(self, *args, **kwargs) -> "MockCallableConfigurator":
        self.call_arguments_matcher = SpecificCallArgumentsMatcher.from_values_and_matchers(args=args, kwargs=kwargs)
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