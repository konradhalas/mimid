class A:
    def __init__(self):
        self.attr = None

    def method(self, param: int) -> int:
        return param

    @property
    def prop(self):
        return None


def function(param: int) -> int:
    return param


class Error(Exception):
    pass
