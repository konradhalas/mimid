from typing import Optional, List

from mimid.common import CallArguments
from mimid.matchers.call import CallArgumentsMatcher
from mimid.exceptions import WrongNumberOfCallsException


class MockAttributeVerifier:
    def __init__(self, calls: List[CallArguments]) -> None:
        self.call_arguments_matcher: Optional[CallArgumentsMatcher] = None
        self.calls_arguments = calls

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call_arguments_matcher = CallArgumentsMatcher.from_values_and_matchers(args=args, kwargs=kwargs)
        return self

    def called(self, times: Optional[int] = None):
        matches = 0
        if self.call_arguments_matcher:
            for call_arguments in self.calls_arguments:
                if self.call_arguments_matcher.match(call_arguments):
                    matches += 1
        if (
            (not self.call_arguments_matcher and not self.calls_arguments)
            or (self.call_arguments_matcher and times is None and matches == 0)
            or (self.call_arguments_matcher and times is not None and matches != times)
            or (not self.call_arguments_matcher and times is not None and len(self.calls_arguments) != times)
        ):
            raise WrongNumberOfCallsException()
