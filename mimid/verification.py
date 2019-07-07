from typing import Optional, List

from mimid.common import CallArguments
from mimid.matchers.call import SpecificCallArgumentsMatcher, AnyCallArgumentsMatcher, CallArgumentsMatcher
from mimid.exceptions import WrongNumberOfCallsException


class MockAttributeVerifier:
    def __init__(self, calls: List[CallArguments]) -> None:
        self.call_arguments_matcher: CallArgumentsMatcher = AnyCallArgumentsMatcher()
        self.calls_arguments = calls

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call_arguments_matcher = SpecificCallArgumentsMatcher.from_values_and_matchers(args=args, kwargs=kwargs)
        return self

    def called(self, times: Optional[int] = None):
        matches = 0
        for call_arguments in self.calls_arguments:
            if self.call_arguments_matcher.match(call_arguments):
                matches += 1
        if (times is None and matches == 0) or (times is not None and matches != times):
            raise WrongNumberOfCallsException()
