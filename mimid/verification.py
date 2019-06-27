from typing import Optional, Union, Any, List

from mimid.exceptions import WrongNumberOfCallsException
from mimid.configuration import MockCallable, Mock, Call


class MockAttributeVerifier:
    def __init__(self, calls: List[Call]) -> None:
        self.call: Optional[Call] = None
        self.calls = calls

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call = Call(args=args, kwargs=kwargs)
        return self

    def called(self, times: Optional[int] = None):
        if (
            (not self.call and not self.calls)
            or (self.call and times is None and self.call not in self.calls)
            or (self.call and times is not None and self.calls.count(self.call) != times)
            or (not self.call and times is not None and len(self.calls) != times)
        ):
            raise WrongNumberOfCallsException()


def verify(target: Union[MockCallable, Mock, Any]) -> MockAttributeVerifier:
    if isinstance(target, MockCallable):
        return MockAttributeVerifier(target.calls)
    elif isinstance(target, Mock):
        return MockAttributeVerifier(target.mock_callable.calls)
    raise TypeError()
