class MimidException(Exception):
    pass


class CallNotConfiguredException(MimidException):
    pass


class WrongNumberOfCallsException(MimidException):
    pass


class ValueNotCapturedException(MimidException):
    pass


class NotMatchingSignatureException(MimidException):
    pass
