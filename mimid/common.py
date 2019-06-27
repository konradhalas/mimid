class Call:
    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other) -> bool:
        return self.args == other.args and self.kwargs == other.kwargs
