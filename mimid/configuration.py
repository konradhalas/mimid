from typing import Optional, Any, List, Dict, Callable

from mimid.common import Call
from mimid.exceptions import CallNotConfiguredException


class CallConfiguration:
    def __init__(
        self,
        call: Optional[Call],
        return_values: Optional[List[Any]] = None,
        exception: Optional[Exception] = None,
        callable: Optional[Callable[[], Any]] = None,
    ) -> None:
        self.call = call
        self.exception = exception
        self.return_values = return_values
        self.callable = callable

    def match(self, call: Call) -> bool:
        return not self.call or self.call == call

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
        self.call: Optional[Call] = None

    def with_args(self, *args, **kwargs) -> "MockCallableConfigurator":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def returns(self, value: Any) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_values=[value]))

    def raises(self, exception: Exception) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, exception=exception))

    def returns_many(self, values: List[Any]) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_values=values))

    def execute(self, callable: Callable[[], Any]):
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, callable=callable))
