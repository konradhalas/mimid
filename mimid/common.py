import inspect
from typing import Callable, Any, MutableMapping


class CallArguments:
    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs

    def bind(self, target: Callable) -> MutableMapping[str, Any]:
        signature = inspect.signature(target)
        return signature.bind(*self.args, **self.kwargs).arguments
