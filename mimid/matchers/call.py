import abc
from typing import Tuple, Dict, Union, Any

from mimid.common import CallArguments
from mimid.matchers.value import ValueMatcher


class CallArgumentsMatcher(abc.ABC):
    @abc.abstractmethod
    def match(self, arguments: CallArguments) -> bool:
        pass


class SpecificCallArgumentsMatcher(CallArgumentsMatcher):
    def __init__(self, args: Tuple[ValueMatcher, ...], kwargs: Dict[str, ValueMatcher]) -> None:
        self.args = args
        self.kwargs = kwargs

    def match(self, arguments: CallArguments) -> bool:
        if len(self.args) != len(arguments.args):
            return False
        for arg_matcher, arg in zip(self.args, arguments.args):
            if not arg_matcher(arg):
                return False
        if self.kwargs.keys() != arguments.kwargs.keys():
            return False
        for arg_name, value in arguments.kwargs.items():
            arg_matcher = self.kwargs[arg_name]
            if not arg_matcher(value):
                return False
        return True

    @staticmethod
    def from_values_and_matchers(
        args: Tuple[Union[ValueMatcher, Any], ...], kwargs: Dict[str, Union[ValueMatcher, Any]]
    ) -> "SpecificCallArgumentsMatcher":
        args_matchers = [ValueMatcher.from_maybe_value(arg) for arg in args]
        return SpecificCallArgumentsMatcher(args=tuple(args_matchers), kwargs=kwargs)


class AnyCallArgumentsMatcher(CallArgumentsMatcher):
    def match(self, arguments: CallArguments) -> bool:
        return True
