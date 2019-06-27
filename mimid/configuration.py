from typing import Optional, Any, List, Dict

from mimid.common import Call
from mimid.exceptions import CallNotConfiguredException


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
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_value=value, exception=None))

    def raises(self, exception: Exception) -> None:
        self.mock_callable.add_configuration(CallConfiguration(call=self.call, return_value=None, exception=exception))
