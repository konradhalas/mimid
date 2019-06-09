import pytest

from mimid import mock, every, CallNotConfiguredException, verify, NotCalledException


class A:
    def foo(self, a, b):
        return a + b


def test_mock_method_call_should_return_configured_value():
    obj = mock(A)
    every(obj.foo).returns(5)

    result = obj.foo(2, 2)

    assert result == 5


def test_not_configured_mock_method_call_should_raise_exception():
    obj = mock(A)

    with pytest.raises(CallNotConfiguredException):
        obj.foo(2, 2)


def test_mock_method_call_with_different_args_should_raise_exception():
    obj = mock(A)
    every(obj.foo).with_args(1, 1).returns(3)

    with pytest.raises(CallNotConfiguredException):
        obj.foo(2, 2)


def test_mock_method_call_with_configured_args_should_return_configured_value():
    obj = mock(A)
    every(obj.foo).with_args(2, 2).returns(5)

    result = obj.foo(2, 2)

    assert result == 5


def test_verify_of_not_called_mock_method_should_raise_exception():
    obj = mock(A)
    every(obj.foo).returns(5)

    with pytest.raises(NotCalledException):
        verify(obj.foo).called_once()


def test_verify_of_called_mock_method_should_not_raise_exception():
    obj = mock(A)
    every(obj.foo).returns(5)

    obj.foo(2, 2)

    try:
        verify(obj.foo).called_once()
    except NotCalledException:
        pytest.fail("Should not raise exception")


def test_verify_of_called_mock_method_with_matching_args_should_not_raise_exception():
    obj = mock(A)
    every(obj.foo).returns(5)

    obj.foo(2, 2)

    try:
        verify(obj.foo).with_args(2, 2).called_once()
    except NotCalledException:
        pytest.fail("Should not raise exception")


def test_verify_of_called_mock_method_with_different_args_should_raise_exception():
    obj = mock(A)
    every(obj.foo).returns(5)

    obj.foo(2, 2)

    with pytest.raises(NotCalledException):
        verify(obj.foo).with_args(1, 3).called_once()
