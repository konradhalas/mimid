from typing import Union

from mimid.common import CallArguments
from mimid.configuration import MockCallable
from mimid.exceptions import WrongNumberOfCallsException
from mimid.matchers.call import SpecificCallArgumentsMatcher, AnyCallArgumentsMatcher, CallArgumentsMatcher
from mimid.matchers.value import ValueMatcher, gt


class MockAttributeVerifier:
    def __init__(self, mock_callable: MockCallable) -> None:
        self.mock_callable = mock_callable
        self.call_arguments_matcher: CallArgumentsMatcher = AnyCallArgumentsMatcher()

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call_arguments_matcher = SpecificCallArgumentsMatcher(
            target=self.mock_callable.target, arguments=CallArguments(args=args, kwargs=kwargs)
        )
        return self

    def called(self, times: Union[int, ValueMatcher] = gt(0)):
        times_matcher = ValueMatcher.from_maybe_value(times)
        matches = 0
        for call_arguments in self.mock_callable.calls_arguments:
            if self.call_arguments_matcher.match(call_arguments):
                matches += 1
        if not times_matcher(matches):
            raise WrongNumberOfCallsException()
