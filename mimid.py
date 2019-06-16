from typing import TypeVar, Type, Union, Any, Optional, List, Dict, cast

T = TypeVar("T")


class Call:
    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other) -> bool:
        return self.args == other.args and self.kwargs == other.kwargs


class CallConfiguration:
    def __init__(self, call: Optional[Call], return_value: Any) -> None:
        self.call = call
        self.return_value = return_value

    def match(self, call: Call) -> bool:
        return not self.call or self.call == call


class MockAttribute:
    def __init__(self, attr: str) -> None:
        self.attr = attr
        self.call_configurations: List[CallConfiguration] = []
        self.calls: List[Call] = []

    def __call__(self, *args, **kwargs) -> Any:
        call = Call(args=args, kwargs=kwargs)
        self.calls.append(call)
        for call_configuration in self.call_configurations:
            if call_configuration.match(call):
                return call_configuration.return_value
        raise CallNotConfiguredException()

    def add_call_configuration(self, call_configuration: CallConfiguration) -> None:
        self.call_configurations.append(call_configuration)

    def verify_call(self, call: Optional["Call"]) -> None:
        if (not call and not self.calls) or (call and call not in self.calls):
            raise NotCalledException()


class Mock:
    def __init__(self, target) -> None:
        self.target = target
        self.mock_attrs: Dict[str, MockAttribute] = {}

    def __getattr__(self, attr) -> MockAttribute:
        if attr not in self.mock_attrs:
            self.mock_attrs[attr] = MockAttribute(attr)
        return self.mock_attrs[attr]


class MockAttributeConfigurator:
    def __init__(self, mock_attr: MockAttribute) -> None:
        self.mock_attr = mock_attr
        self.call: Optional[Call] = None

    def with_args(self, *args, **kwargs) -> "MockAttributeConfigurator":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def returns(self, value: Any) -> None:
        self.mock_attr.add_call_configuration(CallConfiguration(call=self.call, return_value=value))


class MockAttributeVerifier:
    def __init__(self, mock_attr: MockAttribute) -> None:
        self.mock_attr = mock_attr
        self.call: Optional[Call] = None

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def called(self):
        self.mock_attr.verify_call(self.call)


def mock(target: Type[T]) -> T:
    return cast(T, Mock(target))


def every(mock_attr: Union[MockAttribute, Any]) -> MockAttributeConfigurator:
    return MockAttributeConfigurator(mock_attr)


def verify(mock_attr: Union[MockAttribute, Any]) -> MockAttributeVerifier:
    return MockAttributeVerifier(mock_attr)


class MimidException(Exception):
    pass


class CallNotConfiguredException(MimidException):
    pass


class NotCalledException(MimidException):
    pass
