import abc
import inspect
from typing import Tuple, Dict, Callable

from mimid.common import CallArguments
from mimid.exceptions import NotMatchingSignatureException
from mimid.matchers.value import ValueMatcher


class CallArgumentsMatcher(abc.ABC):
    @abc.abstractmethod
    def match(self, arguments: CallArguments) -> bool:
        pass


class SpecificCallArgumentsMatcher(CallArgumentsMatcher):
    def __init__(self, target: Callable, args: Tuple[ValueMatcher, ...], kwargs: Dict[str, ValueMatcher]) -> None:
        self.target = target
        args_matchers = [ValueMatcher.from_maybe_value(arg) for arg in args]
        kwargs_matchers = {key: ValueMatcher.from_maybe_value(value) for key, value in kwargs.items()}
        self.args = args_matchers
        self.kwargs = kwargs_matchers
        signature = inspect.signature(self.target)
        try:
            signature.bind(*self.args, **self.kwargs)
        except TypeError:
            raise NotMatchingSignatureException()

    def match(self, arguments: CallArguments) -> bool:
        try:
            signature = inspect.signature(self.target)
            call_args_binding = signature.bind(*arguments.args, **arguments.kwargs)
            matchers_args_binding = signature.bind(*self.args, **self.kwargs)
            for arg in signature.parameters:
                value = call_args_binding.arguments[arg]
                matcher = matchers_args_binding.arguments[arg]
                if not matcher(value):
                    return False
            return True
        except TypeError:
            return False


class AnyCallArgumentsMatcher(CallArgumentsMatcher):
    def match(self, arguments: CallArguments) -> bool:
        return True
