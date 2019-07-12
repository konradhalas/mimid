import abc
from typing import Callable

from mimid.common import CallArguments
from mimid.exceptions import NotMatchingSignatureException
from mimid.matchers.value import ValueMatcher


class CallArgumentsMatcher(abc.ABC):
    @abc.abstractmethod
    def match(self, arguments: CallArguments) -> bool:
        pass


class SpecificCallArgumentsMatcher(CallArgumentsMatcher):
    def __init__(self, target: Callable, arguments: CallArguments) -> None:
        self.target = target
        self.arguments = arguments
        try:
            self.arguments.bind(self.target)
        except TypeError:
            raise NotMatchingSignatureException()

    def match(self, arguments: CallArguments) -> bool:
        try:
            call_args_binding = arguments.bind(self.target)
            matchers_args_binding = self.arguments.bind(self.target)
            for arg in call_args_binding:
                value = call_args_binding[arg]
                matcher = matchers_args_binding[arg]
                matcher = ValueMatcher.from_maybe_value(matcher)
                if not matcher(value):
                    return False
            return True
        except TypeError:
            return False


class AnyCallArgumentsMatcher(CallArgumentsMatcher):
    def match(self, arguments: CallArguments) -> bool:
        return True
