import pytest

from mimid import mock, every, WrongNumberOfCallsException, verify, gt
from tests.targets import A, function
from tests.utils import not_raises


def test_mock_method_verify_raises_exception_when_method_not_called():
    obj = mock(A)
    every(obj.method).returns(2)

    with pytest.raises(WrongNumberOfCallsException):
        verify(obj.method).called()


def test_mock_method_verify_does_not_raise_exception_when_method_called():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).called()


def test_mock_method_verify_does_not_raise_exception_when_method_called_with_matching_arguments():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).with_args(1).called()


def test_mock_method_verify_does_not_raise_exception_when_method_called_with_matching_kwargs_arguments():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(param=1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).with_args(param=1).called()


def test_mock_method_verify_raises_exception_when_method_called_with_non_matching_arguments():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(2)

    with pytest.raises(WrongNumberOfCallsException):
        verify(obj.method).with_args(1).called()


def test_mock_method_verify_raises_exception_when_method_called_different_number_of_times():
    obj = mock(A)
    every(obj.method).returns(2)
    obj.method(1)

    with pytest.raises(WrongNumberOfCallsException):
        verify(obj.method).called(times=2)


def test_mock_method_verify_does_not_raise_exception_when_method_called_defined_number_of_times():
    obj = mock(A)
    every(obj.method).returns(2)
    obj.method(1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).called(times=1)


def test_mock_method_verify_does_not_raise_exception_when_method_called_defined_number_of_times_with_matching_args():
    obj = mock(A)
    every(obj.method).returns(2)
    obj.method(1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).with_args(1).called(times=1)


def test_mock_method_verify_raises_exception_when_method_called_different_number_of_times_with_matching_args():
    obj = mock(A)
    every(obj.method).returns(2)
    obj.method(1)

    with pytest.raises(WrongNumberOfCallsException):
        verify(obj.method).with_args(1).called(times=2)


def test_mock_function_verify_raises_exception_when_method_not_called():
    func = mock(function)
    every(func).returns(2)

    with pytest.raises(WrongNumberOfCallsException):
        verify(func).called()


def test_mock_function_verify_does_not_raise_exception_when_method_called():
    func = mock(function)
    every(func).returns(2)

    func(1)

    with not_raises(WrongNumberOfCallsException):
        verify(func).called()


def test_mock_function_verify_does_not_raise_exception_when_method_called_with_matching_arguments():
    func = mock(function)
    every(func).returns(2)

    func(1)

    with not_raises(WrongNumberOfCallsException):
        verify(func).with_args(1).called()


def test_mock_function_verify_raises_exception_when_method_called_with_non_matching_arguments():
    func = mock(function)
    every(func).returns(2)

    func(2)

    with pytest.raises(WrongNumberOfCallsException):
        verify(func).with_args(1).called()


def test_mock_method_verify_does_not_raise_exception_when_verify_with_matching_matcher():
    obj = mock(A)
    every(obj.method).returns(2)

    obj.method(1)
    obj.method(1)

    with not_raises(WrongNumberOfCallsException):
        verify(obj.method).called(times=gt(1))


def test_verify_should_raises_exception_when_called_with_non_mock_object():
    with pytest.raises(TypeError):
        verify(1)
