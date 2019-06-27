from typing import Optional, Any, List, Union, Dict, cast, Type, TypeVar

from mimid.exceptions import CallNotConfiguredException, WrongNumberOfCallsException


class Call:
    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other) -> bool:
        return self.args == other.args and self.kwargs == other.kwargs


class CallConfiguration:
    def __init__(self, call: Optional[Call], return_value: Any, exception: Optional[Exception]) -> None:
        self.call = call
        self.exception = exception
        self.return_value = return_value

    def match(self, call: Call) -> bool:
        return not self.call or self.call == call

    def execute(self) -> Any:
        if self.exception:
            raise self.exception
        return self.return_value


class MockCallable:
    def __init__(self) -> None:
        self.call_configurations: List[CallConfiguration] = []
        self.calls: List[Call] = []

    def __call__(self, *args, **kwargs) -> Any:
        call = Call(args=args, kwargs=kwargs)
        self.calls.append(call)
        for call_configuration in self.call_configurations:
            if call_configuration.match(call):
                return call_configuration.execute()
        raise CallNotConfiguredException()

    def add_configuration(self, call_configuration: CallConfiguration) -> None:
        self.call_configurations.append(call_configuration)

    def verify(self, call: Optional["Call"], times: Optional[int]) -> None:
        if (
            (not call and not self.calls)
            or (call and times is None and call not in self.calls)
            or (call and times is not None and self.calls.count(call) != times)
            or (not call and times is not None and len(self.calls) != times)
        ):
            raise WrongNumberOfCallsException()


class Mock:
    def __init__(self, target) -> None:
        self.target = target
        self.mock_attr_callable: Dict[str, MockCallable] = {}
        self.mock_callable = MockCallable()

    def __getattr__(self, attr) -> MockCallable:
        if attr not in self.mock_attr_callable:
            self.mock_attr_callable[attr] = MockCallable()
        return self.mock_attr_callable[attr]

    def __call__(self, *args, **kwargs):
        return self.mock_callable(*args, **kwargs)


class MockCallableConfigurator:
    def __init__(self, mock_callable: MockCallable) -> None:
        self.mock_callable = mock_callable
        self.call: Optional[Call] = None

    def with_args(self, *args, **kwargs) -> "MockCallableConfigurator":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def returns(self, value: Any) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_value=value, exception=None))

    def raises(self, exception: Exception) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_value=None, exception=exception))


T = TypeVar("T")


def mock(target: Type[T]) -> T:
    return cast(T, Mock(target))


def every(target: Union[MockCallable, Mock, Any]) -> MockCallableConfigurator:
    if isinstance(target, MockCallable):
        return MockCallableConfigurator(target)
    elif isinstance(target, Mock):
        return MockCallableConfigurator(target.mock_callable)
    raise TypeError()
