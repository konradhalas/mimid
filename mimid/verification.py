from typing import Optional, Union, Any

from mimid.configuration import MockCallable, Mock, Call


class MockAttributeVerifier:
    def __init__(self, mock_callable: MockCallable) -> None:
        self.mock_callable = mock_callable
        self.call: Optional[Call] = None

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def called(self, times: Optional[int] = None):
        self.mock_callable.verify(call=self.call, times=times)


def verify(target: Union[MockCallable, Mock, Any]) -> MockAttributeVerifier:
    if isinstance(target, MockCallable):
        return MockAttributeVerifier(target)
    elif isinstance(target, Mock):
        return MockAttributeVerifier(target.mock_callable)
    raise TypeError()
