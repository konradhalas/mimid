from contextlib import contextmanager

import pytest

from mimid import mock, every, CallNotConfiguredException, verify, NotCalledException


class A:
    def method(self, param: int) -> int:
        return param


def function(param: int) -> int:
    return param


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


def test_mock_method_call_returns_configured_value():
    obj = mock(A)
    every(obj.method).returns(2)

    result = obj.method(1)

    assert result == 2


def test_mock_method_call_raises_exception_when_call_is_not_configured():
    obj = mock(A)

    with pytest.raises(CallNotConfiguredException):
        obj.method(1)


def test_mock_method_call_raises_exception_when_called_with_non_matching_arguments():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)

    with pytest.raises(CallNotConfiguredException):
        obj.method(2)


def test_mock_method_call_returns_configured_value_when_called_with_matching_arguments():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)

    result = obj.method(1)

    assert result == 2


def test_mock_method_call_returns_configured_value_when_called_with_matching_arguments_and_multiple_configurations():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)
    every(obj.method).with_args(3).returns(4)

    result_1 = obj.method(1)
    result_2 = obj.method(3)

    assert result_1 == 2
    assert result_2 == 4


def test_verify_raises_exception_when_method_not_called():
    obj = mock(A)
    every(obj.method).returns(2)

    with pytest.raises(NotCalledException):
        verify(obj.method).called()


def test_verify_does_not_raise_exception_when_method_called():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(1)

    with not_raises(NotCalledException):
        verify(obj.method).called()


def test_verify_does_not_raise_exception_when_method_called_with_matching_arguments():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(1)

    with not_raises(NotCalledException):
        verify(obj.method).with_args(1).called()


def test_verify_raises_exception_when_method_called_with_non_matching_arguments():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(2)

    with pytest.raises(NotCalledException):
        verify(obj.method).with_args(1).called()


def test_mock_function_call_returns_configured_value():
    func = mock(function)
    every(func).returns(2)

    result = func(1)

    assert result == 2


def test_mock_function_call_raises_exception_when_call_is_not_configured():
    func = mock(function)

    with pytest.raises(CallNotConfiguredException):
        func(1)

def test_mock_function_call_raises_exception_when_called_with_non_matching_arguments():
    func = mock(function)
    every(func).with_args(1).returns(2)

    with pytest.raises(CallNotConfiguredException):
        func(2)


def test_mock_function_call_returns_configured_value_when_called_with_matching_arguments():
    func = mock(function)
    every(func).with_args(1).returns(2)

    result = func(1)

    assert result == 2


def test_mock_function_call_returns_configured_value_when_called_with_matching_arguments_and_multiple_configurations():
    func = mock(function)
    every(func).with_args(1).returns(2)
    every(func).with_args(3).returns(4)

    result_1 = func(1)
    result_2 = func(3)

    assert result_1 == 2
    assert result_2 == 4


def test_mock_function_verify_raises_exception_when_method_not_called():
    func = mock(function)
    every(func).returns(2)

    with pytest.raises(NotCalledException):
        verify(func).called()


def test_mock_function_verify_does_not_raise_exception_when_method_called():
    func = mock(function)
    every(func).returns(2)

    func(1)

    with not_raises(NotCalledException):
        verify(func).called()


def test_mock_function_verify_does_not_raise_exception_when_method_called_with_matching_arguments():
    func = mock(function)
    every(func).returns(2)

    func(1)

    with not_raises(NotCalledException):
        verify(func).with_args(1).called()


def test_mock_function_verify_raises_exception_when_method_called_with_non_matching_arguments():
    func = mock(function)
    every(func).returns(2)

    func(2)

    with pytest.raises(NotCalledException):
        verify(func).with_args(1).called()
