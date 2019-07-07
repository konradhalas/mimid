from typing import List, Union

from mimid.common import CallArguments
from mimid.exceptions import WrongNumberOfCallsException
from mimid.matchers.call import SpecificCallArgumentsMatcher, AnyCallArgumentsMatcher, CallArgumentsMatcher
from mimid.matchers.value import ValueMatcher, any, gt


class MockAttributeVerifier:
    def __init__(self, calls: List[CallArguments]) -> None:
        self.call_arguments_matcher: CallArgumentsMatcher = AnyCallArgumentsMatcher()
        self.calls_arguments = calls

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call_arguments_matcher = SpecificCallArgumentsMatcher.from_values_and_matchers(args=args, kwargs=kwargs)
        return self

    def called(self, times: Union[int, ValueMatcher] = gt(0)):
        times_matcher = ValueMatcher.from_maybe_value(times)
        matches = 0
        for call_arguments in self.calls_arguments:
            if self.call_arguments_matcher.match(call_arguments):
                matches += 1
        if not times_matcher(matches):
            raise WrongNumberOfCallsException()
