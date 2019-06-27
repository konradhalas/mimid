from typing import Optional, List

from mimid.common import CallArguments
from mimid.configuration import CallArgumentsMatcher
from mimid.exceptions import WrongNumberOfCallsException


class MockAttributeVerifier:
    def __init__(self, calls: List[CallArguments]) -> None:
        self.call_matcher: Optional[CallArgumentsMatcher] = None
        self.calls_arguments = calls

    def with_args(self, *args, **kwargs) -> "MockAttributeVerifier":
        self.call_matcher = CallArgumentsMatcher(args=args, kwargs=kwargs)
        return self

    def called(self, times: Optional[int] = None):
        matches = 0
        if self.call_matcher:
            for call_arguments in self.calls_arguments:
                if self.call_matcher.match(call_arguments):
                    matches += 1
        if (
            (not self.call_matcher and not self.calls_arguments)
            or (self.call_matcher and times is None and matches == 0)
            or (self.call_matcher and times is not None and matches != times)
            or (not self.call_matcher and times is not None and len(self.calls_arguments) != times)
        ):
            raise WrongNumberOfCallsException()
